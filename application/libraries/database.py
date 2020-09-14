# load flask sub-systems
from flask import escape

# allow dynamic modules
from importlib import import_module

# load application vars
from application.config.database import *


# Generate Database Helper
class DatabaseHelper:
    def __init__(self, driver_name: str):
        self._driver = driver_name
        pass

    # -----

    def clean_dict(self, dict_object: dict):
        for key in dict_object:
            if 'dict' not in type(dict_object[key]):
                if '_id' not in key or self._driver != 'mongodb':
                    dict_object[key] = escape(dict_object[key])
                else:
                    dict_object[key] = db.o_id(dict_object[key])
            else:
                dict_object[key] = self.clean_dict(dict_object[key])

        return dict_object


database_helper = DatabaseHelper(config['driver'])

# load driver
database = import_module('application.libraries.db_drivers.' + config['driver'])

# load database
config.pop('driver', None)
db = database