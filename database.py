import sqlite3
from werkzeug.security import generate_password_hash

def get_connection():

    return sqlite3.connect("bookings.db")



