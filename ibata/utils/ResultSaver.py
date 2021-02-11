import csv
import json

from ibata.utils.MyJSONEncoder import MyJSONEncoder


class ResultSaver:
    """Class that handles result saving based on output format"""

    @staticmethod
    def save_result(save_as, categories_summary=None, output_format=None):
        """
        Saves result in selected format

        :param save_as: Format in which output should be save. Can be NONE, TXT, JSON and CSV
        :param categories_summary: CategoriesSummary class that should be saved
        :param output_format: Output format of text result. Works only with TXT save_as
        """
        if save_as != "NONE" and save_as is not None:
            if save_as == "TXT":
                text = categories_summary.to_string(output_format, True)
                with open(f"{categories_summary.date_from}_{categories_summary.date_to}.txt", 'w') as file:
                    file.write(text)
            elif save_as == "JSON":
                with open(f"{categories_summary.date_from}_{categories_summary.date_to}.json", 'w') as file:
                    json.dump(categories_summary.categories, file, skipkeys=True, cls=MyJSONEncoder, ensure_ascii=False)
            elif save_as == "CSV":
                with open(f"{categories_summary.date_from}_{categories_summary.date_to}.csv", 'w') as file:
                    csvwriter = csv.writer(file)
                    csvwriter.writerow(["Date", "Account", "Bank code", "Amount", "Currency", "Category",
                                        "Message for payee", "Operation type", "Executor", "Note",
                                        "User identification"])
                    for category in categories_summary.categories:
                        for transaction in category.transactions:
                            csvwriter.writerow([transaction.date, transaction.account, transaction.bank_code,
                                                transaction.amount, transaction.currency, transaction.category,
                                                transaction.message_for_payee, transaction.operation_type,
                                                transaction.executor, transaction.note,
                                                transaction.user_identification])
            return True
        return False
