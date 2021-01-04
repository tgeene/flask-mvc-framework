# load py systems
from typing import Union

# load flask sub-systems
from pymongo import MongoClient

# load ObjectID system
from bson import ObjectId


class Driver:
    """Database driver for handling MongoDB connections."""
    _collection = ""
    _database = ""
    _table = {}
    _where = {}
    _data = {}

    def __init__(self, host: str, port: str, db: str, auth: Union[bool, str] = False, user: str = '', pw: str = '') -> None:
        """Load Driver and setup connection from config."""
        self._host = host
        self._port = port
        self._auth = auth
        self._user = user
        self._pw = pw

        self.database = db

    # -----

    @property
    def database(self) -> str:
        """Get name of current database."""
        return self._database

    @database.setter
    def database(self, database_name: str) -> None:
        """Set name of database and update connection."""
        self._database = database_name

        self.__connect_to_client()

    # -----

    @property
    def __client_url(self) -> str:
        """Generate database connection url."""
        url = self._host + ":" + str(self._port) + '/' + self._auth
        if self._user and self._pw:
            url = self._user + ":" + self._pw + "@" + url

        return "mongodb://" + url

    def __connect_to_client(self) -> None:
        """Create database connection."""
        self.__client = MongoClient(self.__client_url)

        self._db = self.__client[self.database]

    # -----

    @property
    def collection(self) -> object:
        """Get collection connection variable."""
        return self._db[self._collection]

    @collection.setter
    def collection(self, collection_name: str) -> None:
        """Set current collection to use."""
        self._collection = collection_name

    # -----

    @property
    def where(self) -> dict:
        """Get where dict."""
        return self._where

    @where.setter
    def where(self, where_obj: dict) -> None:
        """Set where dict."""
        self._where = where_obj

    @property
    def data(self) -> dict:
        """Get data dict."""
        return self._data

    @data.setter
    def data(self, data_obj: dict) -> None:
        """Set data dict."""
        self._data = data_obj

    # -----

    @staticmethod
    def o_id(id_str: str = '') -> object:
        """Return an Object ID from give string."""
        return ObjectId(id_str)

    # -----

    def get_one(self, collection_name: str, where_obj: Union[dict, list] = None) -> dict:
        """Get single matching database result."""
        self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.find_one(self.where)

    def get(self, collection_name: str, where_obj: Union[dict, list] = None) -> dict:
        """Get all matching database results."""
        self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.find(self.where)

    def get_count(self, collection_name: str, where_obj: Union[dict, list] = None) -> int:
        """Get count of all matching database results."""
        self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.count_documents(self.where)

    # -----

    def aggregate(self, collection_name: str, pipeline: list = None, options: dict = None) -> dict:
        """Get all matching database results using aggregate."""
        self.collection = collection_name

        if pipeline is None:
            pipeline = []

        if options is None:
            options = {}

        return self.collection.aggregate(pipeline, options)

    # -----

    def insert_one(self, collection_name: str, data_obj: dict = None) -> str:
        """Insert one database record."""
        self.collection = collection_name

        if data_obj:
            self.data = data_obj

        return self.collection.insert_one(self.data).inserted_id

    def insert_many(self, collection_name: str, data_obj: list = None) -> list:
        """Insert multiple database records."""
        self.collection = collection_name

        if data_obj:
            self.data = data_obj

        return self.collection.insert_many(self.data).inserted_ids

    # -----

    def update(self, collection_name: str, where_obj: Union[dict, list] = None, data_obj: dict = None) -> int:
        """Update all matching database records."""
        self.collection = collection_name

        if where_obj:
            self.where = where_obj

        if data_obj:
            self.data = data_obj

        return self.collection.update_many(self.where, self.data).modified_count

    # -----

    def delete_one(self, collection_name: str, where_obj: Union[dict, list] = None) -> int:
        """Delete one matching database record."""
        self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.delete_one(self.where).deleted_count

    def delete_many(self, collection_name: str, where_obj: Union[dict, list] = None) -> int:
        """Delete all matching database records."""
        self.collection = collection_name

        if where_obj:
            self.where = where_obj

        return self.collection.delete_many(self.where).deleted_count
