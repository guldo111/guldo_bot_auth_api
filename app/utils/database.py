import os
from psycopg2 import connect

def get_database_connection():
    """
    Provides a connection to the database.
    
    Yields:
        Any: Database connection object.
    """
    conn = connect(os.getenv("DATABASE_URL"))
    try:
        yield conn
    finally:
        conn.close()