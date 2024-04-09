import sqlite3


def createTable(location: str, table: str, columns):
        """
        Creates the database table
        :return: None
        """
        sql = 'create table if not exists ' + table + (columns)
        conn, cursor = create_connection(location)
        cursor.execute(sql)
        conn.commit()
        conn.close()

def create_connection(location: str):
    """
    Creates a connection to the database and a cursor for that connection
    :return: Tuple of a connection and a cursor
    """
    connection = sqlite3.connect(location)
    cursor = connection.cursor()
    return connection, cursor


def clear_database(location: str, table: str): 
      sql = f'drop table {table}'
      conn, cursor = create_connection(location)
      cursor.execute(sql)
      conn.commit()
      conn.close()