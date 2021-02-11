import requests


class TransactionDownloader:
    """
    Base Class for TransactionDownloader. Every class that downloads transactions from BankAPI should inherit this class.
    Every Bank should have its owen {BankName}TransactionDownloader which inherit this class.
    """

    def __init__(self, session=None):
        self.session = self.create_session(session)

    def get_transactions(self, date_from, date_to):
        """
        Downloads transactions from bank API, converts then to array of Transaction objects and returns them

        :param date_from: date from the transaction should be downloaded. Format is YYYY-MM-DD
        :param date_to: date to the transaction should be downloaded. Format is YYYY-MM-DD
        """
        pass

    def create_session(self, s=None):
        """
        Creates requests session

        :param s: provided session, mostly for testing purposes
        :return: session
        """
        session = s or requests.Session()
        session.headers = {'User-Agent': 'Python'}
        return session
