import os
from configparser import ConfigParser

import betamax
from flexmock import flexmock
import pytest

from ibata.Transaction import Transaction
from ibata.downloaders.FioTransactionDownloader import FioTransactionDownloader

try:
    TOKEN = os.environ['FIO_TOKEN']
    NAME = os.environ['NAME']
    ACCOUNTID = os.environ['ACCOUNTID']
    IBAN = os.environ['IBAN']
    BIC = os.environ['BIC']
    NAME_LC = os.environ['NAME_LC']
except KeyError:
    TOKEN = "TOKEN"
    NAME = "JOHN"
    NAME_LC = "John"
    ACCOUNTID = "ACCOUNTID"
    IBAN = "IBAN"
    BIC = "BIC"

with betamax.Betamax.configure() as config:
    if 'FIO_TOKEN' in os.environ:
        # If the tests are invoked with an AUTH_FILE environ variable
        TOKEN = os.environ['FIO_TOKEN']
        # Always re-record the cassetes
        # https://betamax.readthedocs.io/en/latest/record_modes.html
        config.default_cassette_options['record_mode'] = 'once'
    else:
        TOKEN = 'false_token'
        # Do not attempt to record sessions with bad fake token
        config.default_cassette_options['record_mode'] = 'none'

    # Hide the token in the cassettes
    config.define_cassette_placeholder('<TOKEN>', TOKEN)
    config.define_cassette_placeholder('<NAME>', NAME)
    config.define_cassette_placeholder('<NAME>', NAME_LC)
    config.define_cassette_placeholder('<IBAN>', IBAN)
    config.define_cassette_placeholder('<ACCOUNTID>', ACCOUNTID)
    config.define_cassette_placeholder('<BIC>', BIC)
    # tell Betamax where to find the cassettes
    # make sure to create the directory
    config.cassette_library_dir = 'tests/fixtures/cassettes'
    # config.default_cassette_options['record_mode'] = 'new_episodes'


@pytest.fixture
def fio_downloader(config_file, betamax_session):
    flexmock(ConfigParser, get=TOKEN)
    return FioTransactionDownloader(config_file, betamax_session)


def test_get_transactions(fio_downloader):
    transactions = fio_downloader.get_transactions("2020-01-01", "2020-01-05")
    assert len(transactions) == 4
    for transaction in transactions:
        assert type(transaction) == Transaction

    assert transactions[0].date == "2020-01-01"
    assert transactions[0].amount == -516.28
    assert transactions[1].date == "2020-01-02"
    assert transactions[1].amount == 5000.0
    assert transactions[2].date == "2020-01-05"
    assert transactions[2].amount == -563.86
    assert transactions[3].date == "2020-01-05"
    assert transactions[3].amount == -84.0
