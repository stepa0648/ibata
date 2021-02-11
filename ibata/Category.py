class Category:
    """
    Class representing category of transaction
    """

    def __init__(self, name, name_pretty, transactions=None):
        """
        Creates a Category

        :param name: name of a category - in english and lowercase
        :param name_pretty: name of a category in pretty format: will be visible on output. Can be in other languages.
        :param transactions: list of transactions assigned into this category
        """
        self.name = name
        self.name_pretty = name_pretty
        self.amount = 0
        if transactions is not None:
            for transaction in transactions:
                self.amount += transaction.amount
            self.transactions = transactions
        else:
            self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.amount += transaction.amount
