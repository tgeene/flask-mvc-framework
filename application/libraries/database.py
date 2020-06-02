# load flask sub-systems
from flask import escape

# allow dynamic modules
from importlib import import_module

# load application vars
from application.config.database import *

# Generate Database Helper
class DatabaseHelper:
    def __init__(self, driver_name):
        self.driver = driver_name
        pass

    # -----

    @property
    def driver(self):
        return self.__driver

    @driver.setter
    def driver(self, driver_name):
        self.__driver = driver_name

    # -----

    def clean_dict(self, dict_object):
        for key in dict_object:
            if key != '_id' or self.driver != 'mongodb':
                dict_object[key] = escape(dict_object[key])
            else:
                dict_object[key] = db.o_id(dict_object[key])

        return dict_object

database_helper = DatabaseHelper(config['driver'])

# load driver
database = import_module('application.libraries.db_drivers.' + config['driver'])

# load database
config.pop('driver', None)
db = database.Driver(**config)