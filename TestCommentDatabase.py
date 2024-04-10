from comment.Comment import Message
from comment.commentdatabase import CommentDatabase

import testingutils

table = "comments"    
location = "./videoDatabasetest.db"
columns = '(id INTEGER PRIMARY KEY AUTOINCREMENT, video_id INTEGER, comment TEXT, FOREIGN KEY(video_id) REFERENCES videos(id))'

def before():
    testingutils.clear_database(location, table)
    # creates table
    return CommentDatabase("test")

def test_add_message_no_comments_exist(video_id: str, message: Message, comment_db): 
    comment_db.add_message(video_id, message)
    comments = comment_db.get_messages(video_id)
    for m in comments.messages: 
        if m.message == message.message: 
            return True

    return False

def test_add_message_comments_exist(video_id: str, message: Message, comment_db): 
    new_message = Message("user2", "This is another message", 1)
    test_add_message_no_comments_exist(video_id, message, comment_db)
    testingutils.createTable(location, table, columns)
    comment_db.add_message(video_id, new_message)
    comments = comment_db.get_messages(video_id)
    for m in comments.messages: 
        if m.message == new_message.message: 
            return True
    
    return False

if __name__ == '__main__': 
    comment_db = before()

    test_message = Message("user", "This is a test message", 1)
    print(f"result test_add_message_no_comments_exit: {test_add_message_no_comments_exist('1', test_message, comment_db)}")
    print(f"result test_add_message_comments_exist: {test_add_message_comments_exist('1', test_message, comment_db)}")