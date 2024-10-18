# app/utils/database.py

from psycopg2 import connect
import os

def get_database_connection():
    """
    Yields a connection to the database.

    Yields:
        Any: Database connection object.
    """
    conn = connect(os.getenv("DATABASE_URL"))
    try:
        yield conn
    finally:
        conn.close()