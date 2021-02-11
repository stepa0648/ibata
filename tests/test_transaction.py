import pytest

from ibata.Transaction import Transaction


def test_add_transaction(category, transaction):
    category_amount = category.amount
    transaction_cnt = len(category.transactions)
    category.add_transaction(transaction)
    assert category.amount == category_amount + transaction.amount
    assert len(category.transactions) == transaction_cnt + 1


def test_transaction_constructor():
    date = "2020-01-10"
    account = "4526448"
    bank_code = "0300"
    amount = 145.52
    currency = "CZK"
    message_for_payee = "Nákup Alza.cz"
    operation_type = "Platba kartou"
    executor = "John Doe"
    note = "Redukce"
    user_identification = None
    transaction = Transaction(date, account, bank_code, amount, currency, message_for_payee, operation_type, executor,
                              note, user_identification)
    assert transaction.date == date
    assert transaction.account == account
    assert transaction.bank_code == bank_code
    assert transaction.amount == amount
    assert transaction.currency == currency
    assert transaction.message_for_payee == message_for_payee
    assert transaction.operation_type == operation_type
    assert transaction.executor == executor
    assert transaction.note == note
    assert transaction.user_identification == user_identification
    assert transaction.category is None
    assert transaction.get_full_bank_account() == f"{account}/{bank_code}"


def test_get_data_for_analysis(transaction):
    data = transaction.get_data_for_analysis()
    assert data == ["Alza.cz", "Sluchátka v alze"]


@pytest.mark.parametrize('full', (True, False))
def test_to_string(transaction, full):
    text = ""
    if full:
        text = "2020-01-05                               -443.25 CZK electronics     Platba kartou                  " \
               "John Doe                  Alza.cz Sluchátka v alze "
    else:
        text = "2020-01-05 -443.25 CZK electronics Sluchátka v alze Platba kartou None"
    print(transaction.to_string(full))
    assert transaction.to_string(full) == text
