import configparser
import json
from pathlib import Path

from ibata.utils.Helper import Helper


class CategoriesManager:
    """
    Class that handles categories modification
    More info about state transitions is in documentation in :ref:`categories-editing`.
    """

    @staticmethod
    def __get_categories_file_from_config(config_file):
        """
        Return categories file name from config file

        :param config_file: Name of config file, where categories file is defined
        :return: File name of categories file
        """
        config_parser = configparser.ConfigParser()
        config_parser.read(config_file)
        categories_file = config_parser.get('Categories', 'file')
        if Path(categories_file).is_absolute():
            file_path = categories_file
        else:
            file_path = (Path(config_file).parent / categories_file).resolve()
        return file_path

    @staticmethod
    def get_categories_from_config_file(config_file):
        """
        Gets categories from categories file which is defined in config file

        :param config_file: name of config file in which is name of categories file
        :return: list of categories into which transactions will be divided
        """
        file_path = CategoriesManager.__get_categories_file_from_config(config_file)
        with open(file_path, 'r') as json_file:
            categories = json.load(json_file)
        return categories

    @staticmethod
    def set_categories_into_file(config_file, categories):
        """
        Writes categories into category file described in config file

        :param config_file: Name of config file
        :param categories: categories to be written in categories file
        """
        file_path = CategoriesManager.__get_categories_file_from_config(config_file)
        with open(file_path, 'w') as json_file:
            json.dump(categories, json_file, ensure_ascii=False)

    @staticmethod
    def print_categories(categories):
        """Prints categories for user to select from"""
        print("Categories:\n")
        i = 0
        for category in categories:
            print(f'{i}: {category["name"]}')
            i += 1
        print()

    @staticmethod
    def select_category(categories, state):
        """
        First state of categories managing. Serves as selector for category selection, category adding and exit.

        State = 0
        :param categories: list of all categories that can be modified
        :param state: state of categories manager
        :return category_index of selected category (if not selected None is returned) and state of categories manager
        """
        category_index = None
        CategoriesManager.print_categories(categories)
        print("Type:")
        print("category number to edit it")
        print("a to add new category")
        print("s to save and exit")
        input_str = Helper.get_input("x to exit without saving: ")
        if input_str == "s":
            state = 3
        elif input_str == "x":
            state = 4
        elif input_str == "a":
            state = 5
        else:
            try:
                category_index = int(input_str)
            except ValueError as e:
                print("Invalid category number")
                return category_index, state
            if category_index < 0 or category_index >= len(categories):
                print("Invalid category number")
            else:
                state = 1
        return category_index, state

    @staticmethod
    def print_category_detail(category):
        """
        Prints category details
        """
        print("Category:")
        print()
        print(category["name"])
        print(category["name_pretty"])
        print(category["data"])
        print("Type:")
        print("0 to edit category")
        print("1 to delete it")

    @staticmethod
    def category_detail(categories, category_index, state):
        """
        Provides info about given category and info how to edit it or remove.

        state = 1

        :param categories: list of all categories that can be modified
        :param category_index: index of selected category in categories
        :param state: state of categories manager

        :return modified categories and state of categories manager
        """
        CategoriesManager.print_category_detail(categories[category_index])
        input_str = Helper.get_input("2 to return to category select: ")
        if input_str == "0":
            state = 2
        elif input_str == "1":
            categories.pop(category_index)
            state = 0
        elif input_str == "2":
            state = 0
        else:
            print("Invalid option")
        return categories, state

    @staticmethod
    def print_edit_category(category):
        """Prints info about editing category"""
        print()
        print("Editing category:")
        print()
        print(f'name: {category["name"]}')
        print(f'name pretty: {category["name_pretty"]}')
        print(f'key words:')
        j = 0
        for word in category["data"]:
            print(f" {j}: {word}")
            j += 1
        print()
        print("Type:")
        print("0 to edit name")
        print("1 to edit name pretty")
        print("2 to add word to Key words")
        print("3 to remove word from Key words")

    @staticmethod
    def edit_category(categories, category_index, state):
        """
        Provides info how to edit category, how to change its names,
        how to add keyword to this category and how to remove keyword from this category

        state = 2

        :param categories: list of all categories that can be modified
        :param category_index: index of selected category in categories
        :param state: state of categories manager

        :return modified categories and state of categories manager
        """
        CategoriesManager.print_edit_category(categories[category_index])
        input_str = Helper.get_input("4 to return to category: ")
        if input_str == "0":
            name = Helper.get_input("Type new name:")
            categories[category_index]["name"] = name
            state = 1
        elif input_str == "1":
            name_pretty = Helper.get_input("Type new pretty name: ")
            categories[category_index]["name_pretty"] = name_pretty
            state = 1
        elif input_str == "2":
            keyword = Helper.get_input("Type keyword to add: ")
            categories[category_index]["data"].append(keyword)
            state = 1
        elif input_str == "3":
            keyword_index = Helper.get_input("Type keyword number to remove: ")
            try:
                keyword_index = int(keyword_index)
            except ValueError as e:
                print("Invalid keyword number")
                return categories, state
            if keyword_index < 0 or keyword_index >= len(categories[category_index]["data"]):
                print("Invalid keyword number")
            else:
                categories[category_index]["data"].pop(keyword_index)
                state = 1
        elif input_str == "4":
            state = 1
        else:
            print("Invalid option")
        return categories, state

    @staticmethod
    def add_category(categories):
        """
        Provides info and possibility to add new category

        state = 5

        :param categories: list of all categories that can be modified

        :return modified categories with one category added, keywords are empty and can be added in category edit.
        """
        name = Helper.get_input("Type name (english lowercase): ")
        name_pretty = Helper.get_input("Type pretty name (name that will be shown in output/reports): ")
        category = {
            "name": name,
            "name_pretty": name_pretty,
            "data": []
        }
        categories.append(category)
        state = 0
        return categories, state

    @staticmethod
    def edit_categories(config_file, state=0):
        """
        Handles CategoriesManager states. There are 6 states and transition between them can be found in documentation
        in :ref:`categories-editing`.

        States:
            * state 0 - Select category - select category, or select to add category, or exit
            * state 1 - Category detail
            * state 2 - Category edit
            * state 3 - Save and exit
            * state 4 - exit without saving
            * state 5 - add new category

        :param config_file: name of config file where name of categories file can be found
        :param state: only for testing - leave default
        """
        print("Editation mode enabled")
        save = False
        categories = CategoriesManager.get_categories_from_config_file(config_file)
        category_index = None
        while True:
            print()
            if state == 0:
                category_index, state = CategoriesManager.select_category(categories, state)
            elif state == 1:
                categories, state = CategoriesManager.category_detail(categories, category_index, state)
            elif state == 2:
                categories, state = CategoriesManager.edit_category(categories, category_index, state)
            elif state == 3:
                save = True
                break
            elif state == 4:
                save = False
                break
            elif state == 5:
                categories, state = CategoriesManager.add_category(categories)
            else:
                state = 0
        if save:
            CategoriesManager.set_categories_into_file(config_file, categories)
