# load flask sub-systems
from flask_pymongo import PyMongo

# load application vars
from application import system

class Driver:
    def __init__(self, db_config):
        self.config = db_config
        self.connect()

    def connect(self):
        url = self.config['host'] + ":" + self.config['port'] + "/" + self.config['database']
        if self.config['authorize']:
            url = self.config['username'] + ":" + self.config['password'] + "@" + url
        system.config["MONGO_URI"] = "mongodb://" + url

        self.mongo = PyMongo(system)

    def get(self, collection, where = {}, multi = False):
        col = self.mongo.db[collection]

        if multi:
            cursor = col.find(where)
        else:
            cursor = col.find_one(where)

        return cursor
