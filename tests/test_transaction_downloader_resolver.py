import pytest

from ibata.downloaders.FioTransactionDownloader import FioTransactionDownloader
from ibata.downloaders.TransactionDownloaderResolver import TransactionDownloaderResolver


def test_get_transaction_downloader(config_file):
    downloader = TransactionDownloaderResolver.get_transaction_downloader(config_file, "FIO")
    assert type(downloader) == FioTransactionDownloader


@pytest.mark.parametrize('bank', ("fio", "POKUS", "SDA", ""))
def test_get_transaction_downloader(config_file, bank):

    with pytest.raises(SystemExit):
        TransactionDownloaderResolver.get_transaction_downloader(config_file, bank)