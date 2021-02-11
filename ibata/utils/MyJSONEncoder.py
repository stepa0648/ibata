import json
from json import JSONEncoder

from ibata.Category import Category
from ibata.Transaction import Transaction


class MyJSONEncoder(json.JSONEncoder):
    """Custom JSONEncoder for encoding Category and Transaction objects"""

    def default(self, obj):
        if isinstance(obj, Category):
            return obj.__dict__
        elif isinstance(obj, Transaction):
            return obj.__dict__
        return super(JSONEncoder, self).default(obj)
