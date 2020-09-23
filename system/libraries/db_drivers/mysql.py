# load py systems
from typing import Union

# load flask sub-systems
import pymysql.cursors


# Generate MySQL Driver
class Driver:
    # Establish Class Variables
    _table = {}
    _where = {}
    _data = {}

    # Initiate Class
    def __init__(self, host: str, port: str, db: str, auth: Union[bool, str] = False, user: str = '', pw: str = ''):
        self._host = host
        self._port = port
        self._db = db
        self._auth = auth
        self._user = user
        self._pw = pw

        self.__connect_to_client()

    # -----

    # Connect to DB
    def __connect_to_client(self):
        self._connection = pymysql.connect(host=self._host,
                                           port=self._port,
                                           user=self._user,
                                           password=self._pw,
                                           db=self._db,
                                           charset='utf8',
                                           cursorclass=pymysql.cursors.DictCursor)

    # -----

    # Get Table Name
    @property
    def table(self):
        return self._table

    # Set Table Name
    @table.setter
    def table(self, table_name: str):
        self._table = table_name

    # -----

    # Get Where str
    @property
    def where(self):
        return self.__where_builder(self._where)

    # Set Where dict
    @where.setter
    def where(self, where_obj: Union[dict, list]):
        self._where = where_obj

    # Build Where str
    def __where_builder(self, this_obj: Union[dict, list], this_join: str = 'AND'):
        where_statement = ''
        for key, val in this_obj:
            if where_statement:
                where_statement += f" {this_join} "

            val_type = type(val)
            if 'dict' in val_type:
                where_statement += f"({self.__where_builder(val, key)})"
            elif 'list' in val_type:
                where_statement += f"{key} IN({val})"
            elif any(v_type in type(val) for v_type in ['bool', 'int', 'float']):
                where_statement += f"{key} = {val}"
                where_statement = where_statement + key + " = " + val
            elif 'string' in val_type:
                where_statement += f"{key} = '{val}'"

        return where_statement if where_statement else 1

    # -----

    # Get Data dict
    @property
    def data(self):
        return self._data

    # Set Data dict
    @data.setter
    def data(self, data_obj: dict):
        self._data = data_obj

    # -----

    # Get Single Matching DB Result
    def get_one(self, table_name: str, where_obj: Union[dict, list] = None, col_select: str = '*'):
        self.table = table_name

        if where_obj:
            self.where = where_obj

        query = f"SELECT {col_select} FROM {self.table} WHERE {self.where}"

        with self._connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()

    # Get All Matching DB Results
    def get(self, table_name: str, where_obj: Union[dict, list] = None, col_select: str = '*'):
        self.table = table_name

        if where_obj:
            self.where = where_obj

        query = f"SELECT {col_select} FROM {self.table} WHERE {self.where}"

        with self._connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    # Get Count of Matching DB Results
    def get_count(self, table_name: str, where_obj: Union[dict, list] = None):
        self.table = table_name

        if where_obj:
            self.where = where_obj

        query = f"SELECT COUNT(*) AS rows FROM {self.table} WHERE {self.where}"

        with self._connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return result['rows']

    # -----

    # Insert One DB Record
    def insert_one(self, table_name: str, data_obj: dict = None):
        self.table = table_name

        if data_obj:
            self.data = data_obj

        self.__set_insert_vars(self.data)
        query = f"INSERT INTO {self.table} ({self.__col_columns}) VALUES ({self.__col_values})"

        with self._connection.cursor() as cursor:
            cursor.execute(query)

        self._connection.commit()

    # Insert Multiple DB Records
    def insert_many(self, table_name: str, data_obj: list = None):
        self.table = table_name

        if data_obj:
            self.data = data_obj

        self.__set_insert_vars(self.data[0])
        query = f"INSERT INTO {self.table} ({self.__col_columns}) VALUES ({self.__col_values})"

        next(self.data)
        for row in self.data:
            self.__set_insert_vars(row)
            query += f", ({self.__col_values})"

        with self._connection.cursor() as cursor:
            cursor.execute(query)

        self._connection.commit()

    # Build Insert str
    def __set_insert_vars(self, this_data: dict = None):
        col_columns = ''
        col_values = ''
        for key, val in this_data:
            if col_columns or col_values:
                col_columns += ", "
                col_values += ", "

            col_columns += key

            if 'string' in type(val):
                col_values += f"'{val}'"
            elif any(v_type in type(val) for v_type in ['bool', 'int', 'float']):
                col_values += f"{val}"

        self.__col_columns = col_columns
        self.__col_values = col_values

    # -----

    # Update All Matching DB Records
    def update(self, table_name: str, where_obj: Union[dict, list] = None, data_obj: dict = None):
        self.table = table_name

        if where_obj:
            self.where = where_obj

        if data_obj:
            self.data = data_obj

        set_columns = ''
        for key, val in self.data:
            if set_columns:
                set_columns += ", "

            if 'string' in type(val):
                set_columns += f"{key} = '{val}'"
            elif any(v_type in type(val) for v_type in ['bool', 'int', 'float']):
                set_columns += f"{key} = {val}"

        query = f"UPDATE {self.table} SET {set_columns} WHERE {self.where}"

        with self._connection.cursor() as cursor:
            cursor.execute(query)

        self._connection.commit()

    # -----

    # Delete All Matching DB Records
    def delete(self, table_name: str, where_obj: Union[dict, list] = None):
        self.table = table_name

        if where_obj:
            self.where = where_obj

        query = f"DELETE FROM {self.table} WHERE {self.where}"

        with self._connection.cursor() as cursor:
            cursor.execute(query)

        self._connection.commit()
