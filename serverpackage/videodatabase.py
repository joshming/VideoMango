import sqlite3
from sqlite3 import Connection, Cursor

from typing import List, Tuple, Any

LOCATION = "videoDatabase.db"
TABLE = "videos"
ID = "id"
TITLE = "title"
LENGTH = "length"


def create_connection() -> tuple[Connection, Cursor]:
    """
    Creates a connection to the database and a cursor for that connection
    :return: Tuple of a connection and a cursor
    """
    connection = sqlite3.connect(LOCATION)
    cursor = connection.cursor()
    return connection, cursor


def _createTable() -> None:
    """
    Creates the database table
    :return: None
    """
    sql = 'create table if not exists ' + TABLE + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, file TEXT)'
    conn = sqlite3.connect(LOCATION)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


class VideoDatabase:
    """
    Opens up the connection to the CDN video database

    this likely doesn't need to be a class, but whatever
    """

    def __init__(self):
        _createTable()

    def upload(self, title: str, file: str) -> None:
        conn, cursor = create_connection()
        sql = f'insert into videos (title, file) values (\"{title}\", \"{file}\")'
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def fetch(self, id: int) -> str:
        conn, cursor = create_connection()
        sql = f"select title, file from videos where id={id}"
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def checkTitle(self, title: str) -> bool:
        conn, cursor = create_connection()
        sql = f"select * from videos where title=\"{title}\""
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return True if result else False

    def get_most_recent_file(self) -> str:
        """
        Retrieve the most recent movie
        :return:
        """
        conn, cursor = create_connection()
        sql = f"select MAX(id), file from videos"
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        conn.commit()
        conn.close()
        return result[1]

    def get_all_videos(self) -> List[Tuple[Any]]:
        """
        retrieves all information about the rows
        :return: the rows represented as a list of tuples of any types
        """
        conn, cursor = create_connection()
        sql = f"select id, file from videos"
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def get_video_information(self, id: int) -> Tuple[Any]:
        conn, cursor = create_connection()
        sql = f"select id, file from videos where id={id}"
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return result
