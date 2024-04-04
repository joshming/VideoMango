import sqlite3

from sqlite3 import Connection, Cursor
from typing import Tuple, Any, Union

LOCATION = "videoDatabase.db"
TABLE = "users"


class UserDatabase:

    def __init__(self, port: str):
        self.location = f"videoDatabase{port}.db"

    def create_connection(self) -> tuple[Connection, Cursor]:
        """
        Creates a connection to the database and a cursor for that connection
        :return: Tuple of a connection and a cursor
        """
        connection = sqlite3.connect(LOCATION)
        cursor = connection.cursor()
        return connection, cursor


    def createTable(self) -> None:
        """
        Creates the database table
        :return: None
        """
        sql = 'create table if not exists ' + TABLE + ('(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password '
                                                       'TEXT)')
        conn = sqlite3.connect(LOCATION)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()


    def create_user(self, username: str, password: str) -> bool:
        conn, cursor = self.create_connection()
        sql = f'select * from {TABLE} where username=\"{username}\"'
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        if result:
            return False
        insert_statement = f'insert into {TABLE} (username, password) values (\"{username}\", \"{password}\")'
        cursor.execute(insert_statement)
        conn.commit()
        cursor.close()
        conn.close()
        return True


    def verify_user(self, username: str, password: str) -> bool:
        conn, cursor = self.create_connection()
        sql = f'select password from {TABLE} where username=\"{username}\"'
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        if result:
            return password == result[0]
        return False


    def get_user_information(self, username: str) -> Tuple[Any]:
        conn, cursor = self.create_connection()
        sql = f'select * from {TABLE} where username=\"{username}\"'
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return result
