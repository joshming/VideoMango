import sqlite3

LOCATION = "videoDatabase.db"
TABLE = "videos"
ID = "id"
TITLE = "title"
LENGTH = "length"


class VideoDatabase:
    """
    Opens up the connection to the CDN video database
    """
    def __init__(self):
        self.conn = sqlite3.connect(LOCATION)

    def upload(self, title: str, length: str) -> None:
        cursor = self.conn.cursor()
        sql = f'insert into videos (title, length) values ({title}, {length})'
        cursor.execute(sql)

    def fetch(self, id: int) -> str:
        cursor = self.conn.cursor()
        sql = "select title from videos where id = " + id
        cursor.execute(sql)
        return cursor.fetchone()

    def get_length(self, id: int) -> int:
        pass

def createTable() -> None:
    """
    Creates the database table
    :return: None
    """
    sql = 'create table if not exists ' + TABLE + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, LENGTH INTEGER)'
    conn = sqlite3.connect(LOCATION)
    conn.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    createTable()
