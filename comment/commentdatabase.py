import sqlite3
from sqlite3 import Connection, Cursor
from typing import Union

from comment.Comment import Comment, Message

TABLE = "comments"


class CommentDatabase:

    def __init__(self, port: str):
        self.location = f"videoDatabase{port}.db"
        self.createTable()

    def createTable(self) -> None:
        """
        Creates the database table
        :return: None
        """
        sql = 'create table if not exists ' + TABLE + ('(id INTEGER PRIMARY KEY AUTOINCREMENT, video_id INTEGER, '
                                                       'comment TEXT, FOREIGN KEY(video_id) REFERENCES videos(id))')
        conn, cursor = self.create_connection()
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def create_connection(self) -> tuple[Connection, Cursor]:
        """
        Creates a connection to the database and a cursor for that connection
        :return: Tuple of a connection and a cursor
        """
        connection = sqlite3.connect(self.location)
        cursor = connection.cursor()
        return connection, cursor

    def get_messages(self, video_id: int) -> Union[Comment, None]:
        conn, cursor = self.create_connection()
        sql = f'select comment from {TABLE} where video_id={video_id}'
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        conn.close()
        if not result:
            return None
        comment_dict = eval(result[0])
        return Comment(comment_dict["users"],
                       [Message(message["user"], message["message"], int(message["time"])) for message in
                        comment_dict["messages"]],
                       video_id)

    def add_message(self, video_id: int, message: Message) -> bool:
        """
        Adds a new message to the comments for <video_id> from user <user>
        :param video_id:
        :param user:
        :param message:
        :return:
        """
        conn, cursor = self.create_connection()
        comment = self.get_messages(video_id)
        if comment:
            comment.messages.append(message)
            sql = f'update {TABLE} set comment=\"{str(comment.to_dictionary())}\" where video_id={video_id}'
        else:
            comment = Comment([message.user], [message], video_id)
            sql = f'insert into {TABLE} (video_id, comment) values ({video_id}, \"{str(comment.to_dictionary())}\")'
        cursor.execute(sql)
        conn.commit()
        conn.close()
