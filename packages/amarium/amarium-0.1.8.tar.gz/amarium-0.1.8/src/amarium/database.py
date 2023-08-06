"""
The file collects common CRUD operations interacting with 
databases.  The functions aim to provide a simplified API. 

:author: Julian M. Kleber 
"""

from typing import Optional, Any
import sys

import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine

import pandas as pd


def connect_pg_db(host: str, dbname: str, user: str, password: str) -> None:
    """
    The connect_pg_db function connects to a PostgreSQL database.

    :param host:str: Used to specify the hostname of the server to connect to.
    :param dbname:str: Used to specify the name of the database that you want to connect to.
    :param user:str: Used to specify the user name of the database.
    :param password:str: Used to specify the password for the database.
    :return: A connection object.

    :doc-author: Julian M. Kleber
    """

    if password is not None:
        conn_string = (
            f"host={host}' dbname='{dbname}' user='{user}' password='{password}'"
        )
    else:
        conn_string = f"host={host}' dbname='{dbname}' user='{user}'"
    print("Connecting to database\n	->%s" % (conn_string))

    conn = psycopg2.connect(conn_string)
    return conn


def fetch_data(table: str, where_clause: str, limit: int, rows: str, conn:) -> iter:
    """
    The fetch_data function is used to fetch data from a PostgreSQL database.

    The function takes in the following parameters:


    :param table:str: Used to Specify the table name.
    :param where_clause:str: Used to Filter the data that is returned.
    :param limit:int: Used to Limit the number of rows returned by the query.
    :param rows:str: Used to Specify which columns to return from the query.
    :return: An iterable object.

    :doc-author: Trelent
    """

    cursor = conn.cursor(
        "cursor_unique_name", cursor_factory=psycopg2.extras.DictCursor
    )
    cursor.execute(
        f"SELECT {rows} FROM {table} WHERE {where_clause} LIMIT {limit}")
    row_count = 0
    for row in cursor:
        row_count += 1
        print("row: %s    %s\n" % (row_count, row))


def make_conn_sqla(
    host: str, dbname: str, user: str, port: int, password: Optional[str] = None
) -> Any:
    """
    The make_conn_sqla function creates a connection to the database using SQLAlchemy.

    :param host:str: Used to Specify the host name or ip address of the server.
    :param dbname:str: Used to Specify the name of the database to connect to.
    :param user:str: Used to Specify the username for the database.
    :param port:int: Used to Specify the port number that is used to connect to the database.
    :param password:Optional[str]=None: Used to Make the password parameter optional.
    :return: A connection object.

    :doc-author: Trelent
    """

    if password is None:
        password = ""

    conn_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    db = create_engine(conn_string)
    conn = db.connect()
    return conn


def get_filename_no_ext(filename: str) -> str:
    """
    The get_filename_no_ext function takes a filename as input and returns the filename without its extension.
        For example, if the input is 'myfile.txt', then the output will be 'myfile'.

    :param filename:str: Used to Pass the filename to the function.
    :return: The filename without the extension.

    :doc-author: Trelent
    """

    filename = filename.split(".")
    return filename[0]
