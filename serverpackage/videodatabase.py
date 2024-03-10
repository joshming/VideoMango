import sqlite3

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
        sql = "select title from videos where id= " + id
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
        conn.commit()
        conn.close()
        return result[1]
