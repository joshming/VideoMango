import json
import sqlite3

from sqlite3 import Connection, Cursor
from typing import Tuple, Any, Union

from chat.Comment import Comment, Message

LOCATION = "videoDatabase.db"
TABLE = "chats"


def create_connection() -> tuple[Connection, Cursor]:
    """
    Creates a connection to the database and a cursor for that connection
    :return: Tuple of a connection and a cursor
    """
    connection = sqlite3.connect(LOCATION)
    cursor = connection.cursor()
    return connection, cursor


def createTable() -> None:
    """
    Creates the database table
    :return: None
    """
    sql = 'create table if not exists ' + TABLE + ('(id INTEGER PRIMARY KEY AUTOINCREMENT, video_id INTEGER, '
                                                   'chat TEXT, FOREIGN KEY(video_id) REFERENCES videos(id))')
    conn = sqlite3.connect(LOCATION)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


def get_messages(video_id: int) -> Union[Comment, None]:
    conn = sqlite3.connect(LOCATION)
    cursor = conn.cursor()
    sql = f'select chat from {TABLE} where video_id={video_id}'
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


def add_message(video_id: int, message: Message) -> bool:
    """
    Adds a new message to the chat for <video_id> from user <user>
    :param video_id:
    :param user:
    :param message:
    :return:
    """
    conn = sqlite3.connect(LOCATION)
    cursor = conn.cursor()
    comment = get_messages(video_id)
    if comment:
        comment.messages.append(message)
        sql = f'update {TABLE} set chat=\"{str(comment.to_dictionary())}\" where video_id={video_id}'
    else:
        comment = Comment([message.user], [message], video_id)
        sql = f'insert into {TABLE} (video_id, chat) values ({video_id}, \"{str(comment.to_dictionary())}\")'
    cursor.execute(sql)
    conn.commit()
    conn.close()
