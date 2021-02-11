class CategoriesSummary:
    """Class for representing categories summary. It calculates incomes,
    expenses and cash-flow in given time interval and has list of Categories in given time interval."""

    def __init__(self, categories, date_from, date_to):
        self.incomes = 0
        self.expenses = 0
        self.cash_flow = 0
        self.date_from = date_from
        self.date_to = date_to
        self.categories = categories
        self.__count_basic_info()

    def __count_basic_info(self):
        """Calculates basic info - incomes, expenses and cash-flow"""
        for category in self.categories:
            if category.amount == 0:
                continue
            if category.amount > 0:
                self.incomes += category.amount
            else:
                self.expenses += category.amount
        self.cash_flow = self.incomes + self.expenses

    def print(self, output_format=None):
        """Prints categories summary"""
        print(self.to_string(output_format))

    def to_string(self, output_format=None, full=False):
        """
        Creates string representation of categories summary in dependency on output format and full transaction output.

        :param output_format: Defines what info should be in result. Can be NONE, SUMMARY, CATEGORIES, ALL
        :param full: Defines if the transaction output should be full or only important values. More info in Transaction class.
        :return: string represenatation of Categories summary
        """
        if output_format == "NONE":
            return ""
        result = "Přehled výdajů a příjmů\n"
        result += "\n"
        result += f"Od: {self.date_from}\n"
        result += f"Do: {self.date_to}\n"
        result += "\n"
        result += "{0:10} {1:11.2f} Kč\n".format("Příjmy:", self.incomes)
        result += "{0:10} {1:11.2f} Kč\n".format("Výdaje:", self.expenses)
        result += "{0:10} {1:11.2f} Kč\n".format("Cash-flow:", self.cash_flow)
        result += "\n"
        if output_format == "SUMMARY":
            return result
        for category in self.categories:
            if category.amount == 0:
                continue
            result += "{0:20} {1:11.2f} Kč\n".format(category.name_pretty, category.amount)
            if output_format == "CATEGORIES":
                continue
            for transaction in category.transactions:
                result += f"    {transaction.to_string(full)}\n"
        return result
