import pytest
import pathlib

from click.testing import CliRunner
from flexmock import flexmock
from ibata.CategoriesSummary import CategoriesSummary
from ibata.Category import Category
from ibata.Transaction import Transaction


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def config_dir():
    return pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture
def config_file(config_dir):
    return config_dir / "ibata_ok.cfg"


@pytest.fixture
def config_file_object(config_file):
    return flexmock(name=config_file)


@pytest.fixture
def transaction():
    trans = Transaction("2020-01-05", None, None, -443.25, "CZK", "Alza.cz", "Platba kartou", "John Doe",
                        "Sluchátka v alze", None)
    trans.category = "electronics"
    return trans


@pytest.fixture
def transactions():
    trans1 = Transaction("2020-01-05", None, None, -443.25, "CZK", "Alza.cz", "Platba kartou", "John Doe",
                         "Sluchátka v alze", None)
    trans2 = Transaction("2020-01-15", None, None, -583.25, "CZK", "Obi.cz", "Platba kartou", "John Doe",
                         "Regál v obi", None)
    trans3 = Transaction("2020-01-25", None, None, -1583.25, "CZK", "LIDL DEKUJE ZA NAKUP", "Platba kartou", "John Doe",
                         "Jídlo", None)
    trans4 = Transaction("2020-01-25", "91245123", "0300", 58583.25, "CZK", "Oracle", "Platba převodem", "John Doe",
                         "Výplata", None)
    trans5 = Transaction("2020-01-25", "91245123", "0300", -500, "CZK", "Díky za pomoc", "Platba převodem", "John Doe",
                         "Pomoc od Johnyho", None)
    return [trans1, trans2, trans3, trans4, trans5]


@pytest.fixture
def category(transaction):
    return Category("electronics", "Elektronika", [transaction])


@pytest.fixture
def income_category():
    trans = Transaction("2020-01-05", None, None, 24443.25, "CZK", "Alza.cz", "Platba převodem", "John Doe",
                        "Výplata", None)
    trans.category = "income"
    return Category("income", "Příjem", [trans])


@pytest.fixture
def categories_summary(category):
    trans2 = Transaction("2020-01-20", "99512343", "0300", -1443.25, "CZK", "Obi", "Platba převodem", "John Doe",
                         "Regál do garáže", None)
    trans2.category = "hobby"
    categories = [
        Category("hobby", "Hobby", [trans2]),
        category
    ]
    return CategoriesSummary(categories, "2020-01-01", "2020-02-01")
