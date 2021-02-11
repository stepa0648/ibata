import pytest
from flexmock import flexmock

from ibata.cli_app import *


@pytest.fixture
def category_summary1(category, income_category):
    return CategoriesSummary([category, income_category], "2020-01-01", "2020-02-01")


def test_basic_info(category, category_summary1):
    category_summary = CategoriesSummary([category], "2020-01-01", "2020-02-01")
    assert category_summary.expenses == category.amount
    assert category_summary.incomes == 0
    assert category_summary.cash_flow == category.amount
    assert category_summary.date_from == "2020-01-01"
    assert category_summary.date_to == "2020-02-01"
    category_summary1 = category_summary1
    assert category_summary1.expenses == category_summary1.categories[0].amount
    assert category_summary1.incomes == category_summary1.categories[1].amount
    assert category_summary1.cash_flow == category_summary1.categories[0].amount + category_summary1.categories[
        1].amount
    assert category_summary.date_from == "2020-01-01"
    assert category_summary.date_to == "2020-02-01"


@pytest.mark.parametrize(
    ['output_format', 'full'],
    [
        ("SUMMARY", True),
        ("SUMMARY", False),
        ("CATEGORIES", True),
        ("CATEGORIES", False),
        ("ALL", True),
        ("ALL", False),
        ("NONE", True),
        ("NONE", False),
    ],
)
def test_to_string(category_summary1, output_format, full):
    text = ""
    if output_format == "NONE":
        text = ""
    elif output_format == "SUMMARY":
        text = """Přehled výdajů a příjmů

Od: 2020-01-01
Do: 2020-02-01

Příjmy:       24443.25 Kč
Výdaje:        -443.25 Kč
Cash-flow:    24000.00 Kč

"""
    elif output_format == "CATEGORIES":
        text = """Přehled výdajů a příjmů

Od: 2020-01-01
Do: 2020-02-01

Příjmy:       24443.25 Kč
Výdaje:        -443.25 Kč
Cash-flow:    24000.00 Kč

Elektronika              -443.25 Kč
Příjem                  24443.25 Kč
"""
    elif output_format == "ALL":
        if full:
            text = """Přehled výdajů a příjmů

Od: 2020-01-01
Do: 2020-02-01

Příjmy:       24443.25 Kč
Výdaje:        -443.25 Kč
Cash-flow:    24000.00 Kč

Elektronika              -443.25 Kč
    2020-01-05                               -443.25 CZK electronics     Platba kartou                  John Doe                  Alza.cz Sluchátka v alze 
Příjem                  24443.25 Kč
    2020-01-05                              24443.25 CZK income          Platba převodem                John Doe                  Alza.cz Výplata 
"""
        else:
            text = """Přehled výdajů a příjmů

Od: 2020-01-01
Do: 2020-02-01

Příjmy:       24443.25 Kč
Výdaje:        -443.25 Kč
Cash-flow:    24000.00 Kč

Elektronika              -443.25 Kč
    2020-01-05 -443.25 CZK electronics Sluchátka v alze Platba kartou None
Příjem                  24443.25 Kč
    2020-01-05 24443.25 CZK income Výplata Platba převodem None
"""
    output = category_summary1.to_string(output_format, full)
    print(output)
    print("###################")
    print(text)

    assert category_summary1.to_string(output_format, full) == text
