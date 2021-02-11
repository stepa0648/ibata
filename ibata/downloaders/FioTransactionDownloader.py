import configparser
import sys

import requests

from ibata.Transaction import Transaction
from .TransactionDownloader import TransactionDownloader


class FioTransactionDownloader(TransactionDownloader):
    """
    Class for downloading transaction from Fio Bank API. Documentation can be found on
    https://www.fio.cz/docs/cz/API_Bankovnictvi.pdf
    """

    BASE_URL = "https://www.fio.cz/ib_api/rest/periods/{}/{}/{}/transactions.{}"
    FORMAT = "json"
    CONNECTION_ERROR = "Failed to retrieve transactions from Bank API FIO."

    def __init__(self, config_file, session=None):
        super().__init__(session)
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(config_file)
        self.API_TOKEN = self.config_parser.get('FIO', 'token')

    def __build_url(self, date_from, date_to):
        """Builds URL based on date_from and date_to"""
        return self.BASE_URL.format(self.API_TOKEN, date_from, date_to, self.FORMAT)

    def __get_value_from_api_transaction(self, api_transaction, column_name):
        """
        From api transaction and given column name returs its value. If its value is None return None

        :param api_transaction: transaction downloaded via api
        :param column_name: name of column to get value from
        :return: column value if column is not None, otherwise returns None
        """
        column = api_transaction[column_name]
        if column is None:
            return None
        return column["value"]

    def __create_transaction(self, api_transaction):
        """
        From API transaction creates Transaction object and returns it

        :param api_transaction: API transaction that shoul be transformed to Transaction object
        :return: Transaction object
        """
        return Transaction(
            date=self.__get_value_from_api_transaction(api_transaction, "column0").split("+")[0],
            account=self.__get_value_from_api_transaction(api_transaction, "column2"),
            bank_code=self.__get_value_from_api_transaction(api_transaction, "column3"),
            amount=self.__get_value_from_api_transaction(api_transaction, "column1"),
            currency=self.__get_value_from_api_transaction(api_transaction, "column14"),
            message_for_payee=self.__get_value_from_api_transaction(api_transaction, "column16"),
            operation_type=self.__get_value_from_api_transaction(api_transaction, "column8"),
            executor=self.__get_value_from_api_transaction(api_transaction, "column9"),
            note=self.__get_value_from_api_transaction(api_transaction, "column25"),
            user_identification=self.__get_value_from_api_transaction(api_transaction, "column7")
        )

    def __process_transactions(self, api_transactions):
        """Gets all api transactions and returns then as list of Transaction objects"""
        transactions = []
        for api_transaction in api_transactions:
            transaction = self.__create_transaction(api_transaction)
            transactions.append(transaction)
        return transactions

    def get_transactions(self, date_from, date_to):
        url = self.__build_url(date_from, date_to)
        result = {}
        try:
            result = self.session.get(url)
        except requests.exceptions.ConnectionError as e:
            print(self.CONNECTION_ERROR, file=sys.stderr)
            exit(1)
        if result.status_code != 200:
            print(self.CONNECTION_ERROR, file=sys.stderr)
            exit(1)
        transaction_list = result.json()["accountStatement"]["transactionList"]
        api_transactions = transaction_list["transaction"]
        return self.__process_transactions(api_transactions)
