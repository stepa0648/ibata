import pytest
from flexmock import flexmock

from ibata.cli_app import *
from ibata.utils.Helper import Helper


@pytest.fixture
def categories(config_file):
    return CategoriesManager.get_categories_from_config_file(config_file)


def test_get_categories_from_config_file(config_file):
    categories = CategoriesManager.get_categories_from_config_file(config_file)
    assert len(categories) == 18


def test_set_categories_into_file(runner, config_file, category):
    categories = CategoriesManager.get_categories_from_config_file(config_file)
    category = {
        "name": "newcategory",
        "name_pretty": "Nova kategorie",
        "data": []
    }
    categories.append(category)
    flexmock(CategoriesManager, __get_categories_file_from_config="pokus.json")
    with runner.isolated_filesystem():
        CategoriesManager.set_categories_into_file(config_file, categories)
        categories1 = CategoriesManager.get_categories_from_config_file(config_file)
        assert len(categories) == len(categories1)


@pytest.mark.parametrize('state', (0, 1, 2, 3, 4, 5))
def test_edit_categories(state):
    flexmock(CategoriesManager, get_categories_from_config_file=[])
    config_file = ""
    if state == 0:
        flexmock(CategoriesManager).should_receive("select_category").once().and_return("", 4)
    elif state == 1:
        flexmock(CategoriesManager).should_receive("category_detail").once().and_return("", 4)
    elif state == 2:
        flexmock(CategoriesManager).should_receive("edit_category").once().and_return("", 4)
    elif state == 3:
        flexmock(CategoriesManager).should_receive("set_categories_into_file").once().and_return("")
    elif state == 4:
        flexmock(CategoriesManager).should_receive("set_categories_into_file").times(0)
    elif state == 5:
        flexmock(CategoriesManager).should_receive("add_category").once().and_return("", 4)
    CategoriesManager.edit_categories(config_file, state)


def test_add_category(categories):
    flexmock(Helper).should_receive("get_input").and_return("newcategory").and_return("newcategory1")
    categories_cnt = len(categories)
    categories1, state = CategoriesManager.add_category(categories)
    assert state == 0
    assert len(categories1) == categories_cnt + 1
    assert categories1[-1]["name"] == "newcategory"
    assert categories1[-1]["name_pretty"] == "newcategory1"
    assert categories1[-1]["data"] == []


@pytest.mark.parametrize("option", ("0", "1", "2", "3", "4", "5", "10", "ASdjasnda"))
def test_edit_category(categories, option):
    helper = flexmock(Helper).should_receive("get_input").and_return(option)
    state = 2
    data_cnt = len(categories[0]["data"])
    name = categories[0]["name"]
    name_pretty = categories[0]["name_pretty"]
    text = ""
    if option == "0":
        name = "Name"
        helper.and_return(name)
        state = 1
    elif option == "1":
        name_pretty = "NamePretty"
        helper.and_return(name_pretty)
        state = 1
    elif option == "2":
        helper.and_return("keyword")
        data_cnt += 1
        state = 1
    elif option == "3":
        helper.and_return("0")
        data_cnt -= 1
        state = 1
    elif option == "4":
        state = 1

    categories1, state1 = CategoriesManager.edit_category(categories, 0, 2)
    assert state1 == state
    assert categories1[0]["name"] == name
    assert categories1[0]["name_pretty"] == name_pretty
    assert len(categories1[0]["data"]) == data_cnt


def test_print_edit_category(capsys, categories):
    CategoriesManager.print_edit_category(categories[0])
    captured = capsys.readouterr()
    text = """
Editing category:

name: supermarket
name pretty: Supermarket
key words:
 0: billa
 1: kaufland
 2: rohlík
 3: rohlik
 4: tesco
 5: lidl
 6: albert
 7: penny
 8: globus
 9: zabka
 10: coop

Type:
0 to edit name
1 to edit name pretty
2 to add word to Key words
3 to remove word from Key words
"""
    assert captured.out == text


@pytest.mark.parametrize("option", ("0", "1", "2", "3", "ASdjasnda"))
def test_category_detail(categories, option):
    flexmock(Helper).should_receive("get_input").and_return(option)
    categories_cnt = len(categories)
    categories1, state1 = CategoriesManager.category_detail(categories, 0, 1)
    state = 1
    if option == "0":
        state = 2
    elif option == "1":
        state = 0
        categories_cnt -= 1
    elif option == "2":
        state = 0
    assert categories_cnt == len(categories1)
    assert state1 == state


def test_print_category_detail(capsys, categories):
    CategoriesManager.print_category_detail(categories[0])
    captured = capsys.readouterr()
    text = """Category:

supermarket
Supermarket
['billa', 'kaufland', 'rohlík', 'rohlik', 'tesco', 'lidl', 'albert', 'penny', 'globus', 'zabka', 'coop']
Type:
0 to edit category
1 to delete it
"""
    assert captured.out == text


def test_print_categories(capsys, categories):
    CategoriesManager.print_categories(categories)
    captured = capsys.readouterr()
    assert captured.out == """Categories:

0: supermarket
1: food
2: electronics
3: drugstore
4: accomodation
5: health
6: zverimex
7: household
8: finance
9: insurance
10: transport
11: hobby
12: entertainment
13: books
14: sport
15: flower
16: clothes&shoes
17: saving

"""


@pytest.mark.parametrize("option", ("0", "a", "s", "x"))
def test_select_category(categories, option):
    flexmock(Helper).should_receive("get_input").and_return(option)
    category_index1, state1 = CategoriesManager.select_category(categories, 0)
    if option == "s":
        state = 3
    elif option == "x":
        state = 4
    elif option == "a":
        state = 5
    else:
        state = 1
    assert state == state1
