import re

from ibata.Category import Category
from ibata.utils.CategoriesManager import CategoriesManager


class TransactionAnalyzer:
    """Class for finding category for given transactions"""

    def __init__(self, config_file):
        """
        Creates this class, loads categories from categories file defined in config file and creates categories
        list where transaction are being inserted

        :param config_file: name of config file, where name of categories file can be found
        """
        self.categories_json = CategoriesManager.get_categories_from_config_file(config_file)
        self.categories = []
        for category in self.categories_json:
            self.categories.append(Category(category["name"], category["name_pretty"]))
        self.categories.append(Category("incomes", "Příjmy"))
        self.categories.append(Category("other", "Jiné"))

    def __get_category(self, analysis_data):
        """
        Gets a spending category

        :param analysis_data: data from transaction that should be check for category info
        """
        print("One transaction: ####################################################################################")
        for data in analysis_data:
            transaction_note = data.lower()
            print(f"Checking: {transaction_note}")
            if re.search(r"\[ignore]", transaction_note):
                print("[ignore] found")
                return None
            for category in self.categories_json:
                for shop in category["data"]:
                    if re.search(rf"\b{shop}\b", transaction_note):
                        return category["name"]
        return "other"

    def __get_full_category(self, transaction):
        """
        Gets a transaction category or income category if amount is > 0

        :param transaction: transaction for which category should be returned
        :return: string representation of category of given transaction
        """
        analysis_data = transaction.get_data_for_analysis()
        if transaction.amount < 0:
            return self.__get_category(analysis_data)
        else:
            return "incomes"

    def categorize_transactions(self, transactions):
        """
        Gives every transaction one category and returns them with category parameter filled with name of that category

        :param transactions: transaction to be categorized
        :return: transactions with category parameter filled
        """
        for transaction in transactions:
            transaction.category = self.__get_full_category(transaction)
        return transactions

    def get_categories_from_transactions(self, transactions):
        """
        Assigns categorized transaction to categories, and for every category finds amount spent in this category
        and assign transactions into this categories

        :param transactions: transactions with filled category - if category is not filled, transaction is ignored
        :return: list of categories with transaction and amount
        """
        for transaction in transactions:
            for category in self.categories:
                if transaction.category == category.name:
                    category.add_transaction(transaction)
        return self.categories
