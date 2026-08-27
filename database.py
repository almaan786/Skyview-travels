import os
import sqlite3


def get_connection():
    database_url = os.environ["DATABASE_URL"]

    if database_url.startswith("sqlite:///"):
        database_path = database_url.replace("sqlite:///", "", 1)
        return sqlite3.connect(database_path)

    import psycopg
    return psycopg.connect(database_url)