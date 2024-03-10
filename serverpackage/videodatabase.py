import sqlite3

from typing import List, Tuple, Any

LOCATION = "videoDatabase.db"
TABLE = "videos"
ID = "id"
TITLE = "title"
LENGTH = "length"


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
        conn = sqlite3.connect(LOCATION)
        cursor = conn.cursor()
        sql = f'insert into videos (title, file) values (\"{title}\", \"{file}\")'
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def fetch(self, id: int) -> str:
        conn = sqlite3.connect(LOCATION)
        cursor = conn.cursor()
        sql = f"select file from videos where id={id}"
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def checkTitle(self, title: str) -> bool:
        conn = sqlite3.connect(LOCATION)
        cursor = conn.cursor()
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
        conn = sqlite3.connect(LOCATION)
        cursor = conn.cursor()
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
        conn = sqlite3.connect(LOCATION)
        cursor = conn.cursor()
        sql = f"select id, file from videos"
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def get_video_information(self, id: int) -> Tuple[Any]:
        conn = sqlite3.connect(LOCATION)
        cursor = conn.cursor()
        sql = f"select id, file from videos where id={id}"
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return result
