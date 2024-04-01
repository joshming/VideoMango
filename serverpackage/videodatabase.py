import sqlite3
from sqlite3 import Connection, Cursor

from typing import List, Tuple, Any, Union

LOCATION = "videoDatabase"
TABLE = "videos"
ID = "id"
TITLE = "title"
LENGTH = "length"


def create_connection(port: str) -> tuple[Connection, Cursor]:
    """
    Creates a connection to the database and a cursor for that connection
    :return: Tuple of a connection and a cursor
    """
    connection = sqlite3.connect(LOCATION + port + ".db")
    cursor = connection.cursor()
    return connection, cursor


def _createTable(port: str) -> None:
    """
    Creates the database table
    :return: None
    """
    sql = 'create table if not exists ' + TABLE + ('(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, file TEXT, '
                                                   'size INTEGER)')
    conn = sqlite3.connect(LOCATION + port + ".db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


class VideoDatabase:
    """
    Opens up the connection to the CDN video database

    this likely doesn't need to be a class, but whatever
    """

    recently_added: List[Any]

    def __init__(self, port: str):
        self.port = port
        self.recently_added = []
        _createTable(port)

    def upload(self, title: str, file: str, size: int) -> None:
        conn, cursor = create_connection(self.port)
        sql = f'insert into videos (title, file, size) values (\"{title}\", \"{file}\", {size})'
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        self.recently_added.append((title, size))

    def fetch(self, id_: int) -> str:
        conn, cursor = create_connection(self.port)
        sql = f"select title, file from videos where id={id_}"
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def fetch_by_title(self, title: str) -> str:
        conn, cursor = create_connection(self.port)
        sql = f"select file from videos where title=\"{title}\""
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def checkTitle(self, title: str) -> bool:
        conn, cursor = create_connection(self.port)
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
        conn, cursor = create_connection(self.port)
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
        conn, cursor = create_connection(self.port)
        sql = f"select id, title, file from videos"
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def get_video_information(self, id: int) -> Tuple[Any]:
        conn, cursor = create_connection(self.port)
        sql = f"select id, title, size from videos where id={id}"
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def get_recently_added(self):
        recents = self.recently_added
        self.recently_added = []
        return recents