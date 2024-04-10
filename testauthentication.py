# to test userdatabase.py 
import sqlite3

from authentication.userdatabase import UserDatabase
import testingutils

def before_each():
    table = "users"
    location = "./videoDatabasetest.db"
    
    testingutils.clear_database(location, table)
    # create table
    return UserDatabase("test"), table, location

def test_create_connection():
    comment_db, table, location = before_each()

    connection, cursor = comment_db.create_connection()

    # Check if connection is established
    assert connection is not None, "Connection object is None"
    assert isinstance(connection, sqlite3.Connection), "Connection to SQLite database failed"
    print("Connection to SQLite database successful")
    
    # Check if cursor is created
    assert cursor is not None, "Cursor creation failed"
    print("SUCCESS: Create connection")

    cursor.close()
    connection.close()

def test_create_table():
    comment_db, table, location = before_each()
    comment_db.createTable()
    
    # connect to db
    connection = sqlite3.connect(location)
    cursor = connection.cursor()

    # verify table exists
    sql = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"
    cursor.execute(sql)
    result = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()

    # Check if the table exists
    assert result is not None, "Table does not exist."
    print("SUCCESS: Create table")

def test_create_user():
    comment_db, table, location = before_each()
    
    # connect db
    connection = sqlite3.connect(location)
    cursor = connection.cursor()

    username='john'
    password='pickles'

    result = comment_db.create_user(username, password)

    # verify function respo
    assert result is True, "Create user failed."

    # verify user was created successfully
    sql = f"select username, password from {table} where username='{username}'"
    cursor.execute(sql)
    users_result = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    
    assert users_result == (f'{username}', f'{password}'), "Username and password does not match"
    print("SUCCESS: Create User")

def test_verify_user_with_user_exists():
    comment_db, table, location = before_each()
    
    # connect db
    connection = sqlite3.connect(location)
    cursor = connection.cursor()

    username='john'
    password='pickles'

    # Create user
    testingutils.add_user(connection, cursor, table, username, password)

    # Call functions
    result = comment_db.verify_user(username, password)

    # verify function found
    assert result is True, "Verify user failed."
    print("Verify user when user exist was successful")

def test_verify_user_with_user_not_exists():
    comment_db, table, location = before_each()

    username='johnny'
    password='picklefries'

    # Call functions
    result = comment_db.verify_user(username, password)

    # verify function found
    assert result is False, "Verify user failed."
    print("Verify user when user does not exist was successful")

def get_user_information_user_exists(): 
    comment_db, table, location = before_each()
    
    # connect db
    connection = sqlite3.connect(location)
    cursor = connection.cursor()

    username='pineapple'
    password='juice'

    # Create user
    testingutils.add_user(connection, cursor, table, username, password)

    # Call functions
    users_result = comment_db.get_user_information(username)

    # verify function found
    assert users_result == (1, f'{username}', f'{password}'), "Get user information failed. Username and password does not match"
    print("Get user information when user exists was successful")

def get_user_information_user_does_not_exists(): 
    comment_db, table, location = before_each()
    
    # connect db
    connection = sqlite3.connect(location)
    cursor = connection.cursor()

    username='pineapple'

    # Call functions
    users_result = comment_db.get_user_information(username)

    # verify function found
    assert users_result is None, "Get user information failed. Found a user"
    print("Get user information when user exists was successful")

if __name__ == '__main__': 
    test_create_connection()
    test_create_table()
    test_create_user()
    test_verify_user_with_user_exists()
    test_verify_user_with_user_not_exists()
    get_user_information_user_exists()
    get_user_information_user_does_not_exists()
