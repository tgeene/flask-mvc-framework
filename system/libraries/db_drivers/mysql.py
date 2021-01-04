# load py systems
from typing import Union

# load flask sub-systems
import pymysql.cursors


# Generate MySQL Driver
class Driver:
    """Database driver for handling MySQL connections."""
    _table = {}
    _where = {}
    _data = {}

    # Initiate Class
    def __init__(self, host: str, port: str, db: str, auth: Union[bool, str] = False, user: str = '', pw: str = '') \
            -> None:
        """Load Driver and setup connection from config."""
        self._host = host
        self._port = port
        self._db = db
        self._auth = auth
        self._user = user
        self._pw = pw

        self.__connect_to_client()

    # -----

    def __connect_to_client(self) -> None:
        """Create database connection."""
        self._connection = pymysql.connect(host=self._host,
                                           port=self._port,
                                           user=self._user,
                                           password=self._pw,
                                           db=self._db,
                                           charset='utf8',
                                           cursorclass=pymysql.cursors.DictCursor)

    # -----

    @property
    def table(self) -> str:
        """Get current table in use."""
        return self._table

    @table.setter
    def table(self, table_name: str) -> None:
        """Set current table to use."""
        self._table = table_name

    # -----

    @property
    def where(self) -> Union[dict, list]:
        """Get where string from dict."""
        return self._where

    @where.setter
    def where(self, where_obj: Union[dict, list]) -> None:
        """Set where dict."""
        self._where = where_obj

    def __where_builder(self, this_obj: Union[dict, list], this_join: str = 'AND') -> str:
        """Build where statement from dict."""
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

    @property
    def data(self) -> dict:
        """Get data dict."""
        return self._data

    @data.setter
    def data(self, data_obj: dict) -> None:
        """Set data dict."""
        self._data = data_obj

    # -----

    def get_one(self, table_name: str, where_obj: Union[dict, list] = None, col_select: str = '*') -> Union[dict, None]:
        """Get single matching database result."""
        self.table = table_name

        if where_obj:
            self.where = where_obj

        query = f"SELECT {col_select} FROM {self.table} WHERE {self.__where_builder(self._where)}"

        with self._connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()

    def get(self, table_name: str, where_obj: Union[dict, list] = None, col_select: str = '*') -> list:
        """Get all matching database results."""
        self.table = table_name

        if where_obj:
            self.where = where_obj

        query = f"SELECT {col_select} FROM {self.table} WHERE {self.__where_builder(self._where)}"

        with self._connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_count(self, table_name: str, where_obj: Union[dict, list] = None) -> int:
        """Get count of all matching database results."""
        self.table = table_name

        if where_obj:
            self.where = where_obj

        query = f"SELECT COUNT(*) AS rows FROM {self.table} WHERE {self.__where_builder(self._where)}"

        with self._connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

        return result['rows']

    # -----

    def insert_one(self, table_name: str, data_obj: dict = None) -> int:
        """Insert one database record."""
        self.table = table_name

        if data_obj:
            self.data = data_obj

        self.__set_insert_vars(self.data)
        query = f"INSERT INTO {self.table} ({self.__col_columns}) VALUES ({self.__col_values})"

        self.__run_non_select(query)

        return self._connection.insert_id()

    def insert_many(self, table_name: str, data_obj: list = None) -> int:
        """Insert multiple database records."""
        self.table = table_name

        if data_obj:
            self.data = data_obj

        self.__set_insert_vars(self.data[0])
        query = f"INSERT INTO {self.table} ({self.__col_columns}) VALUES ({self.__col_values})"

        next(self.data)
        for row in self.data:
            self.__set_insert_vars(row)
            query += f", ({self.__col_values})"

        return self.__run_non_select(query)

    def __set_insert_vars(self, this_data: dict = None) -> None:
        """Build insert statement from dict."""
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

    def update(self, table_name: str, where_obj: Union[dict, list] = None, data_obj: dict = None) -> int:
        """Update all matching database records."""
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

        query = f"UPDATE {self.table} SET {set_columns} WHERE {self.__where_builder(self._where)}"

        return self.__run_non_select(query)

    # -----

    def delete(self, table_name: str, where_obj: Union[dict, list] = None) -> int:
        """Delete all matching database records."""
        self.table = table_name

        if where_obj:
            self.where = where_obj

        query = f"DELETE FROM {self.table} WHERE {self.__where_builder(self._where)}"

        return self.__run_non_select(query)

    def __run_non_select(self, query: str) -> int:
        with self._connection.cursor() as cursor:
            affected = cursor.execute(query)

        self._connection.commit()

        return affected
