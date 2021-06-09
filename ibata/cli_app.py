import configparser
import json
import re
import calendar

import click

from ibata.CategoriesSummary import CategoriesSummary
from ibata.TransactionAnalyzer import TransactionAnalyzer
from ibata.downloaders.TransactionDownloaderResolver import TransactionDownloaderResolver
from ibata.utils.CategoriesManager import CategoriesManager
from ibata.utils.PlotMaker import PlotMaker
from ibata.utils.ResultSaver import ResultSaver

CONFIG_FILE = "ibata.cfg"
DEFAULT_BANK = "FIO"
BANKS_METAVAR = list(TransactionDownloaderResolver.BANKS.keys())
FAILED_TO_LOAD_THE_CONFIG = "Failed to load the configuration!"
DEFAULT_OUTPUT_FORMAT = "ALL"
DEFAULT_SAVE_FORMAT = "NONE"


def check_valid_bank(ctx, param, value):
    if value in TransactionDownloaderResolver.BANKS.keys():
        return value
    else:
        raise click.BadParameter(
            f"not valid bank. Must be on of {list(TransactionDownloaderResolver.BANKS.keys())}")


def check_valid_date(ctx, param, value):
    if value is None:
        return value
    if re.match('^((?:19|20)[0-9]{2})-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])$', value):
        return value
    else:
        raise click.BadParameter(
            'not valid date format. Must be YYYY-MM-DD')

def check_valid_year_month(ctx, param, value):
    if value is None:
        return value
    if re.match('^((?:19|20)[0-9]{2})-(0?[1-9]|1[0-2])$', value):
        return value
    else:
        raise click.BadParameter(
            'not valid date format. Must be YYYY-MM')


def check_valid_dates(date_from, date_to):
    if date_from is None:
        raise click.BadParameter(
            'not valid options. Date from is required')
    if date_to is None:
        raise click.BadParameter(
            'not valid options. Date to is required')
    if date_from > date_to:
        raise click.BadParameter(
            'not valid dates. Date from must precede date to.')
    return True


def check_valid_config_file_callback(ctx, param, value):
    if value is None:
        raise click.BadParameter(FAILED_TO_LOAD_THE_CONFIG)
    config_file = value.name
    if config_file == "":
        raise click.BadParameter(FAILED_TO_LOAD_THE_CONFIG)
    config_parser = configparser.ConfigParser()
    try:
        config_parser.read(config_file)
        for key in TransactionDownloaderResolver.BANKS.keys():
            config_parser.get(key, 'token')
        try:
            CategoriesManager.get_categories_from_config_file(config_file)
        except FileNotFoundError as e:
            raise click.BadParameter(FAILED_TO_LOAD_THE_CONFIG +
                                     " Categories file not found: " + e.filename)
        except json.decoder.JSONDecodeError as e:
            raise click.BadParameter(FAILED_TO_LOAD_THE_CONFIG +
                                     f" Categories file not valid json: {e.msg} at row "
                                     f"{str(e.lineno)} column {e.colno}")
    except configparser.NoSectionError as e:
        raise click.BadParameter(FAILED_TO_LOAD_THE_CONFIG + " " + e.message)
    except configparser.NoOptionError as e:
        raise click.BadParameter(FAILED_TO_LOAD_THE_CONFIG + " " + e.message)
    except configparser.MissingSectionHeaderError as e:
        raise click.BadParameter(FAILED_TO_LOAD_THE_CONFIG + " " + e.message.split("\n")[0])
    except configparser.Error as e:
        raise click.BadParameter(FAILED_TO_LOAD_THE_CONFIG)
    return config_file


def validate_output_format(ctx, param, value):
    if re.match('^(SUMMARY|CATEGORIES|ALL|NONE)$', value):
        return value
    else:
        raise click.BadParameter(
            'not valid output format. Must be [SUMMARY|CATEGORIES|ALL|NONE]')


def validate_save_format(ctx, param, value):
    if re.match('^(TXT|JSON|CSV|NONE)$', value):
        return value
    else:
        raise click.BadParameter(
            'not valid save format. Must be [TXT|JSON|CSV]')

def get_dates_from_year_month(year_month):
    date_from = year_month + "-01"
    split_year_month = year_month.split("-")
    date_to = year_month + "-" + str(calendar.monthrange(int(split_year_month[0]), int(split_year_month[1]))[1])
    return date_from, date_to


@click.command()
@click.version_option(version=0.1, help='Show the version and exit.')
@click.option('-c', '--config', metavar='FILENAME', type=click.File('r'),
              callback=check_valid_config_file_callback,
              default=CONFIG_FILE,
              help=f'IBATA configuration file. [default: {CONFIG_FILE}]')
@click.option('-f', '--from', 'date_from', metavar="DATE",
              callback=check_valid_date,
              help='Date from which the transactions are being downloaded and parsed. Format is YYYY-MM-DD. '
                   '[Required if -e and -m flags are missing]')
@click.option('-t', '--to', 'date_to', metavar="DATE",
              callback=check_valid_date,
              help='Date to which the transactions are being downloaded and parsed. Format is YYYY-MM-DD. '
                   '[Required if -e and -m flags are missing]')
@click.option('-m', '--month', 'year_month', metavar="DATE",
              callback=check_valid_year_month,
              help='Year and month from which the transactions are being downloaded and parsed. Format is YYYY-MM.'
                   '[Required if -e, -f and -t flags are missing]')
@click.option('-b', '--bank', default=DEFAULT_BANK, metavar=BANKS_METAVAR,
              callback=check_valid_bank,
              help='Bank from which will be transactions downloaded. Default: FIO')
@click.option('-o', '--output-format', metavar='[SUMMARY|CATEGORIES|ALL|NONE]', default=DEFAULT_OUTPUT_FORMAT,
              help='Verbosity level of the output. works only for output into console or into TXT file.'
                   '  [default: ALL]', callback=validate_output_format)
@click.option('-p', '--plot', is_flag=True,
              help='Should generate plot, show it, and save it in "{date_from}_{date_to}.png"')
@click.option('-s', '--save-as', metavar='[TXT|JSON|CSV|NONE]',
              help='In which format should be result saved. If not present result won\'t be saved.  '
                   'If present, result would be saved into "{date_from}_{date_to}.{save-as}" file.    [default: NONE]',
              default=DEFAULT_SAVE_FORMAT,
              callback=validate_save_format)
@click.option('-e', '--edit', '--edit-categories', is_flag=True,
              help='If present app enters editation mode for categories and other options are ignored.')
def ibata(config, date_from, date_to, year_month, bank, output_format, plot, save_as, edit):
    """A tool for analyzing bank transactions"""
    if edit:
        CategoriesManager.edit_categories(config)
        exit(0)
    if year_month:
        date_from, date_to = get_dates_from_year_month(year_month)
    check_valid_dates(date_from, date_to)
    transaction_downloader = TransactionDownloaderResolver.get_transaction_downloader(config, bank)
    transactions = transaction_downloader.get_transactions(date_from, date_to)
    transaction_analyzer = TransactionAnalyzer(config)
    categorized_transactions = transaction_analyzer.categorize_transactions(transactions)
    categories = transaction_analyzer.get_categories_from_transactions(categorized_transactions)
    categories_summary = CategoriesSummary(categories, date_from, date_to)
    categories_summary.print(output_format)
    PlotMaker.show_and_save_plot(categories_summary, plot)
    ResultSaver.save_result(save_as, categories_summary, output_format)
