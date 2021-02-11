import pytest
from flexmock import flexmock

from ibata.Category import Category
from ibata.cli_app import *


@pytest.fixture
def category_summary1(category, income_category):
    return CategoriesSummary([category, income_category], "2020-01-01", "2020-02-01")


def test_add_transaction(category, transaction):
    category_amount = category.amount
    transaction_cnt = len(category.transactions)
    category.add_transaction(transaction)
    assert category.amount == category_amount + transaction.amount
    assert len(category.transactions) == transaction_cnt + 1


def test_category_constructor(transaction):
    name = "Name"
    name_pretty = "name pretty"
    category = Category(name, name_pretty)
    assert category.name == name
    assert category.name_pretty == name_pretty
    assert category.amount == 0
    assert category.transactions == []

    category1 = Category(name, name_pretty, [transaction, transaction])
    assert category1.name == name
    assert category1.name_pretty == name_pretty
    assert category1.amount == transaction.amount * 2
    assert category1.transactions == [transaction, transaction]
