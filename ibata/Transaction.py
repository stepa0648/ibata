from ibata.utils.Helper import Helper


class Transaction:
    """Class for representing one bank transaction"""

    def __init__(self, date, account, bank_code, amount, currency, message_for_payee, operation_type, executor, note,
                 user_identification):
        self.date = date
        self.account = account
        self.bank_code = bank_code
        self.amount = amount
        self.currency = currency
        self.message_for_payee = message_for_payee
        self.operation_type = operation_type
        self.executor = executor
        self.note = note
        self.user_identification = user_identification
        self.category = None

    def get_full_bank_account(self):
        """Returns bank account/bank code"""
        if self.account is None or self.bank_code is None:
            return None
        return f"{self.account}/{self.bank_code}"

    def get_data_for_analysis(self):
        """
        To change which parameters should be considered in transaction categorization, you need to change this method

        :return: list of text values, which should be considered in transaction categorization
        """
        data = []
        Helper.append_values_if_not_none(data, [self.note, self.message_for_payee, self.user_identification])
        return data

    def print_inline(self):
        """
        Prints one line text representation of transaction
        """
        print(self.to_string())

    def to_string(self, full=False):
        """
        Returns string representation of transaction

        :param full: if all parameters should be in output, or only important ones
        :return: string representation of transaction
        """
        if full:
            return "{:10} {:20} {:4} {:11.2f} {:3} {:15} {:30} {:25} {} {} {}" \
                .format(*map(Helper.none_to_empty, [self.date, self.account, self.bank_code, self.amount, self.currency,
                                                    self.category, self.operation_type, self.executor,
                                                    self.message_for_payee, self.note,
                                                    self.user_identification]))
        else:
            return f"{self.date} {self.amount} {self.currency} {self.category} {self.note} {self.operation_type} " \
                   f"{self.get_full_bank_account()}"

    def print(self):
        """
        Prints text represenation of transaction. One parameter on one line
        """
        print(f"Date: {self.date}")
        print(f"Account: {self.account}")
        print(f"Bank code: {self.bank_code}")
        print(f"Full account: {self.get_full_bank_account()}")
        print(f"Amount: {self.amount}")
        print(f"Currency: {self.currency}")
        print(f"User identification: {self.user_identification}")
        print(f"Message for payee: {self.message_for_payee}")
        print(f"Operation type: {self.operation_type}")
        print(f"Executor: {self.executor}")
        print(f"Note: {self.note}")
        print(f"Category: {self.category}")
