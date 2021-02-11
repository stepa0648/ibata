class Helper:
    """Class with some useful methods"""

    @staticmethod
    def append_values_if_not_none(data, values):
        """
        Appends value from values to given list data, if value is not None
        :param data - list to which values are append
        :param values - values to append
        """
        for value in values:
            if value is not None:
                data.append(value)
        return data

    @staticmethod
    def none_to_empty(value):
        """
        Return value if not None, otherwise return empty string
        """
        if value is None:
            return ""
        return value

    @staticmethod
    def get_input(prompt):
        """
        Make mocking of input function possible
        :param prompt: Prompt to be shown by input function
        """
        return input(prompt)
