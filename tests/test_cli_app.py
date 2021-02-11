import pathlib

import pytest
from flexmock import flexmock

from ibata.cli_app import *
from ibata.downloaders.TransactionDownloader import TransactionDownloader


@pytest.fixture
def start_cli_fake():
    """Prevents starting everything if cli is successful"""
    flexmock(TransactionDownloaderResolver, get_transaction_downloader=0)
    flexmock(TransactionDownloader, get_transactions=0)
    flexmock(TransactionAnalyzer, __init__=0)
    flexmock(TransactionAnalyzer, categorize_transactions=0)
    flexmock(TransactionAnalyzer, get_categories_from_transactions=0)
    flexmock(CategoriesSummary, print=0)
    flexmock(PlotMaker, show_and_save_plot=0)
    flexmock(ResultSaver, save_result=0)


config_dir = pathlib.Path(__file__).parent / "fixtures"


@pytest.mark.parametrize('options', (["-f", "2020-01-01", "-t", "2020-01-01", "-c", config_dir / "ibata_ok.cfg"],
                                     ["-e", "-c", config_dir / "ibata_ok.cfg"]))
def test_ok_required(start_cli_fake, runner, options):
    result = runner.invoke(ibata, options)
    print(result.exit_code)
    assert result.exit_code == 1


def test_valid_bank():
    banks = TransactionDownloaderResolver.BANKS.keys()
    for bank in banks:
        assert bank == check_valid_bank(None, None, bank)


def test_invalid_bank():
    with pytest.raises(click.exceptions.BadParameter):
        check_valid_bank(None, None, "bank")


@pytest.mark.parametrize('date', (None, "2020-01-04", "1994-10-15"))
def test_check_valid_date(date):
    assert date == check_valid_date(None, None, date)


@pytest.mark.parametrize('date', ("None", "20201-01-04", "1994-20-15", "1994-12-35", "1994-10-15-16"))
def test_check_invalid_date(date):
    with pytest.raises(click.exceptions.BadParameter):
        check_valid_date(None, None, date)


@pytest.mark.parametrize(['date_from', 'date_to'],
                         [('2020-01-01', '2020-01-01'), ('2020-01-01', '2020-01-02'), ('2020-01-01', '2021-01-02')])
def test_check_valid_dates(date_from, date_to):
    assert check_valid_dates(date_from, date_to)


@pytest.mark.parametrize(['date_from', 'date_to'],
                         [('2020-01-01', '2019-01-01'), ('2020-02-01', '2020-01-31'), (None, '2021-01-02'),
                          ('2020-02-01', None)])
def test_check_invalid_dates(date_from, date_to):
    with pytest.raises(click.exceptions.BadParameter):
        check_valid_dates(date_from, date_to)


def test_check_valid_config_file_callback(config_file, config_file_object):
    assert config_file == check_valid_config_file_callback(None, None, config_file_object)


@pytest.mark.parametrize('file_name', ("ibata_wrong_categories.cfg", "ibata_not_existing_categories.cfg",
                                       "ibata_no_token.cfg", "ibata_no_fio_section.cfg", "ibata_no_categories_file.cfg",
                                       "ibata_no_categories.cfg"))
def test_check_invalid_config_file_callback(config_dir, file_name):
    config_file = config_dir / file_name
    file = flexmock(name=config_file)
    with pytest.raises(click.exceptions.BadParameter):
        check_valid_config_file_callback(None, None, file)


@pytest.mark.parametrize('output_format', ("SUMMARY", "CATEGORIES", "ALL", "NONE"))
def test_validate_output_format(output_format):
    assert output_format == validate_output_format(None, None, output_format)


@pytest.mark.parametrize('output_format', ("SUMMAR", "", "ANSJA"))
def test_validate_output_format_wrong(output_format):
    with pytest.raises(click.exceptions.BadParameter):
        validate_output_format(None, None, output_format)


@pytest.mark.parametrize('save_format', ("TXT", "JSON", "CSV", "NONE"))
def test_validate_save_format(save_format):
    assert save_format == validate_save_format(None, None, save_format)


@pytest.mark.parametrize('save_format', ("", "JasSON", "CSasV"))
def test_validate_save_format_wrong(save_format):
    with pytest.raises(click.exceptions.BadParameter):
        validate_save_format(None, None, save_format)


@pytest.mark.parametrize('options', (["-c", config_dir / "ibata_ok.cfg"], ["-f", "2020-01-01", "-c", config_dir / "ibata_ok.cfg"],
                                     ["-t", "2020-01-01", "-c", config_dir / "ibata_ok.cfg"]))
def test_missing_required(start_cli_fake, runner, options):
    result = runner.invoke(ibata, options)
    print(result.exit_code)
    assert result.exit_code == 2
    assert "is required" in result.output
