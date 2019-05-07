# load flask sub-systems
import pymysql.cursors

class Driver:
    _where = {}
    _data = {}

    def __init__(self, host, port, database, authorize=False, username='', password=''):
        self._host = host
        self._port = port
        self._database = database
        self._authorize = authorize
        self._username = username
        self._password = password

        self.__connect_to_client()

    # -----

    def __connect_to_client(self):
        self.db = pymysql.connect(host=self._host,
                                  port=self._port,
                                  user=self._username,
                                  password=self._password,
                                  db=self._database,
                                  charset='utf8',
                                  cursorclass=pymysql.cursors.DictCursor)

    # -----

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, table_name):
        self._table = table_name

    # -----

    @property
    def where(self):
        return self.__where_builder(self._where)

    @where.setter
    def where(self, where_obj):
        self._where = where_obj

    def __where_builder(self, this_obj, this_join='AND'):
        where_statement = ''
        for key, val in this_obj:
            if where_statement:
                where_statement += f" {this_join} "

            val_type = type(val)
            if 'dict' in val_type:
                where_statement += f"({self.__where_builder(val, key)})"
            elif 'list' in val_type:
                where_statement += f"{key} IN({val})"
            elif any(v_type in type(var) for v_type in ['bool', 'int', 'float']):
                where_statement += f"{key} = {val}"
                where_statement = where_statement + key + " = " + val
            elif 'string' in val_type:
                where_statement += f"{key} = '{val}'"

        return where_statement if where_statement else 1

    # -----

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data_obj):
        self._data = data_obj

    # -----

    def get_one(self, table_name='', where_obj={}, col_select='*'):
        if table_name:
            self.table = table_name

        if where_obj:
            self.where = where_obj

        query = f"SELECT {col_select} FROM {self.table} WHERE {self.where}"

        with self.db.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()

    def get(self, table_name='', where_obj={}, col_select='*'):
        if table_name:
            self.table = table_name

        if where_obj:
            self.where = where_obj

        query = f"SELECT {col_select} FROM {self.table} WHERE {self.where}"

        with self.db.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_count(self, table_name='', where_obj={}):
        if table_name:
            self.table = table_name

        if where_obj:
            self.where = where_obj

        query = f"SELECT COUNT(*) AS rows FROM {self.table} WHERE {self.where}"

        with self.db.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return result['rows']

    # -----

    def insert_one(self, table_name='', data_obj={}):
        if table_name:
            self.table = table_name

        if data_obj:
            self.data = data_obj

        __set_insert_vars(self.data)
        query = f"INSERT INTO {self.table} ({self.__col_columns}) VALUES ({self.__col_values})"

        with self.db.cursor() as cursor:
            cursor.execute(query)

        self.db.commit()

    def insert_many(self, table_name='', data_obj={}):
        if table_name:
            self.table = table_name

        if data_obj:
            self.data = data_obj

        __set_insert_vars(self.data[0])
        query = f"INSERT INTO {self.table} ({self.__col_columns}) VALUES ({self.__col_values})"

        next(self.data)
        for row in self.data:
            __set_insert_vars(row)
            query += f", ({self.__col_values})"

        with self.db.cursor() as cursor:
            cursor.execute(query)

        self.db.commit()

    def __set_insert_vars(self, this_data):
        col_columns = ''
        col_values = ''
        for key, val in this_data:
            if col_columns or col_values:
                col_columns += ", "
                col_values += ", "

            col_columns += key

            if 'string' in type(val):
                col_values += f"'{val}'"
            elif any(v_type in type(var) for v_type in ['bool', 'int', 'float']):
                col_values += f"{val}"

        self.__col_columns = col_columns
        self.__col_values = col_values

    # -----

    def update(self, table_name='', where_obj={}, data_obj={}):
        if table_name:
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
                set_columns += f"'{key} = {val}'"
            elif any(v_type in type(var) for v_type in ['bool', 'int', 'float']):
                set_columns += f"{key} = {val}"

        query = f"UPDATE {self.table} SET {set_columns} WHERE {self.where}"

        with self.db.cursor() as cursor:
            cursor.execute(query)

        self.db.commit()

    # -----

    def delete(self, table_name='', where_obj={}):
        if table_name:
            self.table = table_name

        if where_obj:
            self.where = where_obj

        query = f"DELETE FROM {self.table} WHERE {self.where}"

        with self.db.cursor() as cursor:
            cursor.execute(query)

        self.db.commit()
