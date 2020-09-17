# load py systems
from typing import Union

# load flask sub-systems
from pymongo import MongoClient

# load ObjectID system
from bson import ObjectId


# Generate MongoDB Driver
class Driver:
    # Establish Class Variables
    _collection = ""
    _table = {}
    _where = {}
    _data = {}

    # Initiate Class
    def __init__(self, host: str, port: str, db: str, auth: Union[bool, str] = False, user: str = '', pw: str = ''):
        self._host = host
        self._port = port
        self._authorize = auth
        self._username = user
        self._password = pw

        self.database = db

    # -----

    # Get DB Name
    @property
    def database(self):
        return self.__database

    # Set DB Name and Change Connection
    @database.setter
    def database(self, database_name: str):
        self.__database = database_name

        self.__connect_to_client()

    # -----

    # Create DB Connect URL by Vars
    @property
    def __client_url(self):
        try:
            url = self._host + ":" + str(self._port) + '/' + self._authorize
            if self._username and self._password:
                url = self._username + ":" + self._password + "@" + url

            return "mongodb://" + url
        except:
            print("Error: Could not generate connection url from config.")

    # Connect to DB
    def __connect_to_client(self):
        self.__client = MongoClient(self.__client_url)

        self._db = self.__client[self.database]

    # -----

    # Get DB Point with Collection
    @property
    def collection(self):
        return self._db[self._collection]

    # Set Collection Name
    @collection.setter
    def collection(self, collection_name: str):
        self._collection = collection_name

    # -----

    # Get Dict
    @property
    def where(self):
        return self._where

    # Set Dict
    @where.setter
    def where(self, where_obj: dict):
        self._where = where_obj

    # Get Dict
    @property
    def data(self):
        return self._data

    # Set Dict
    @data.setter
    def data(self, data_obj: dict):
        self._data = data_obj

    # -----

    # Convert String to Object ID
    @staticmethod
    def o_id(id_str: str = ''):
        return ObjectId(id_str)

    # -----

    # Get Single Matching DB Result
    def get_one(self, collection_name: str, where_obj: Union[dict, list] = None):
        self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.find_one(self.where)

    # Get All Matching DB Results
    def get(self, collection_name: str, where_obj: Union[dict, list] = None):
        self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.find(self.where)

    # Get Count of Matching DB Results
    def get_count(self, collection_name: str, where_obj: Union[dict, list] = None):
        self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.count_documents(self.where)

    # -----

    # Get All Matching DB Results using Aggregate
    def aggregate(self, collection_name: str, pipeline: list = None, options: dict = None):
        self.collection = collection_name

        if pipeline is None:
            pipeline = []

        if options is None:
            options = {}

        return self.collection.aggregate(pipeline, options)

    # -----

    # Insert One DB Record
    def insert_one(self, collection_name: str, data_obj: dict = None):
        self.collection = collection_name

        if data_obj:
            self.data = data_obj

        return self.collection.insert_one(self.data).inserted_id

    # Insert Multiple DB Records
    def insert_many(self, collection_name: str, data_obj: list = None):
        self.collection = collection_name

        if data_obj:
            self.data = data_obj

        return self.collection.insert_many(self.data).inserted_id

    # -----

    # Update All Matching DB Records
    def update(self, collection_name: str, where_obj: Union[dict, list] = None, data_obj: dict = None):
        self.collection = collection_name

        if where_obj:
            self.where = where_obj

        if data_obj:
            self.data = data_obj

        return self.collection.update(self.where, self.data)

    # -----

    # Delete One Matching DB Records
    def delete_one(self, collection_name: str, where_obj: Union[dict, list] = None):
        self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.delete_one(self.where)

    # Delete All Matching DB Records
    def delete_many(self, collection_name: str, where_obj: Union[dict, list] = None):
        self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.delete_many(self.where)
