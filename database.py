import psycopg
import os

def get_connection():
    return psycopg.connect(os.environ["DATABASE_URL"])