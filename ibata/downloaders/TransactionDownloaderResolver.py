import sys

from ibata.downloaders.FioTransactionDownloader import FioTransactionDownloader


class TransactionDownloaderResolver:
    """
    Class that resolves which TransactionDownloader should be used. If new TransactionDownloader is created
    it must be inserted into BANKS here.
    """
    BANKS = {
        "FIO": FioTransactionDownloader
    }

    @staticmethod
    def get_transaction_downloader(config, bank):
        """
        Returns TransactionDownloader based on bank name
        :param config: Config file name
        :param bank: Name of bank
        :return: TransactionDownloader for given Bank
        """
        downloader = None
        try:
            downloader = TransactionDownloaderResolver.BANKS[bank]
        except KeyError as e:
            print("Not valid bank name", file=sys.stderr)
            exit(1)
        return downloader(config)
