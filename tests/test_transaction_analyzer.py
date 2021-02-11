from ibata.Transaction import Transaction
from ibata.cli_app import *


def test_transaction_analyzer_constructor(config_file):
    transaction_analyzer = TransactionAnalyzer(config_file)
    assert len(transaction_analyzer.categories_json) == 18
    assert len(transaction_analyzer.categories_json) + 2 == len(transaction_analyzer.categories)


def test_categorize_transactions(config_file, transactions):
    transaction_analyzer = TransactionAnalyzer(config_file)
    categorized_transactions = transaction_analyzer.categorize_transactions(transactions)
    assert categorized_transactions[0].category == "electronics"
    assert categorized_transactions[1].category == "hobby"
    assert categorized_transactions[2].category == "supermarket"
    assert categorized_transactions[3].category == "incomes"
    assert categorized_transactions[4].category == "other"


def test_categorize_transactions_misleading(config_file):
    trans1 = Transaction("2020-01-05", None, None, -443.25, "CZK", "Balza.cz", "Platba kartou", "John Doe",
                         "Sluchátka v alze", None)
    trans2 = Transaction("2020-01-15", None, None, -583.25, "CZK", ",Obi.cz", "Platba kartou", "John Doe",
                         "Regál v obi", None)

    transactions = [trans1, trans2]
    transaction_analyzer = TransactionAnalyzer(config_file)
    transaction_analyzer.categorize_transactions(transactions)
    assert trans1.category == "other"
    assert trans2.category == "hobby"


def test_get_categories_from_transactions(config_file, transactions):
    transaction_analyzer = TransactionAnalyzer(config_file)
    categorized_transactions = transaction_analyzer.categorize_transactions(transactions)
    categories = transaction_analyzer.get_categories_from_transactions(categorized_transactions)
    assert len(categories) == 20
    for category in categories:
        if category.name in ["electronics", "hobby", "supermarket", "incomes", "other"]:
            assert category.amount != 0
        else:
            assert category.amount == 0
