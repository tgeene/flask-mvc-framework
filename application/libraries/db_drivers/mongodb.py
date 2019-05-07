# load flask sub-systems
from pymongo import MongoClient

# load ObjectID system
from bson import ObjectId

class Driver:
    _where = {}
    _data = {}

    def __init__(self, host, port, database, authorize=False, username='', password=''):
        self._host = host
        self._port = port
        self._authorize = authorize
        self._username = username
        self._password = password

        self.database = database

    # -----

    @property
    def __client_url(self):
        try:
            url = self._host + ":" + self._port  + '/' + self.__database
            if self._authorize:
                url = self._username + ":" + self._password + "@" + url

            return "mongodb://" + url
        except:
            print("Error: Could not generate connection url from config.")

    def __connect_to_client(self):
        self.__client = MongoClient(self.__client_url)

        self.db = self.__client.db

    # -----

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, database_name):
        self.__database = database_name

        self.__connect_to_client()

    # -----

    @property
    def collection(self):
        return self.db[self._collection]

    @collection.setter
    def collection(self, collection_name):
        self._collection = collection_name

    # -----

    @property
    def where(self):
        return self._where

    @where.setter
    def where(self, where_obj):
        self._where = where_obj

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data_obj):
        self._data = data_obj

    # -----

    def _id(self, id = ''):
        return ObjectId(id)

    # -----

    def get_one(self, collection_name='', where_obj={}):
        if collection_name:
            self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.find_one(self.where)

    def get(self, collection_name='', where_obj={}):
        if collection_name:
            self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.find(self.where)

    def get_count(self, collection_name='', where_obj={}):
        if collection_name:
            self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.count_documents(where)

    # -----

    def aggregate(self, collection_name, pipeline, options={}):
        if collection_name:
            self.collection = collection_name

        return self.collection.aggregate(pipeline, options)

    # -----

    def insert_one(self, collection_name='', data_obj={}):
        if collection_name:
            self.collection = collection_name

        if data_obj:
            self.data = data_obj

        return self.collection.insert_one(self.data).inserted_id

    def insert_many(self, collection_name='', data_obj={}):
        if collection_name:
            self.collection = collection_name

        if data_obj:
            self.data = data_obj

        return self.collection.insert_many(self.data).inserted_id

    # -----

    def update(self, collection_name='', where_obj={}, data_obj={}):
        if collection_name:
            self.collection = collection_name

        if where_obj:
            self.where = where_obj

        if data_obj:
            self.data = data_obj

        return self.collection.update(self.where, self.data)

    # -----

    def delete_one(self, collection_name='', where_obj={}):
        if collection_name:
            self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.delete_one(self.where)

    def delete_many(self, collection_name='', where_obj={}):
        if collection_name:
            self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.delete_many(self.where)
