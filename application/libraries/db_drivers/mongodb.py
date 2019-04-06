# load flask sub-systems
from flask_pymongo import PyMongo

# load application vars
from application import system

# load ObjectID system
from bson import ObjectId

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

    def _id(self, id = ''):
        return ObjectId(id)

    def get(self, collection, where = {}, multi = False):
        col = self.mongo.db[collection]

        if multi:
            return col.find(where)
        else:
            return col.find_one(where)

    def get_count(self, collection, where = {}):
        col = self.mongo.db[collection]

        return col.count_documents(where)

    def aggregate(self, collection, pipeline, options = {}):
        col = self.mongo.db[collection]

        return col.aggregate(pipeline, options)

    def insert(self, collection, data, multi = False):
        col = self.mongo.db[collection]

        if multi:
            return col.insert_many(data).inserted_ids
        else:
            return col.insert_one(data).inserted_id

    def update(self, collection, where, data):
        col = self.mongo.db[collection]

        col.update(where, data)

    def delete(self, collection, where, multi = False):
        col = self.mongo.db[collection]

        if multi:
            return col.delete_many(where)
        else:
            return col.delete_one(where)
