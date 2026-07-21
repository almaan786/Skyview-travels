import sqlite3
from werkzeug.security import generate_password_hash

connection = sqlite3.connect("bookings.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    package TEXT,

    departure_city TEXT,

    travel_date TEXT,

    full_name TEXT,

    phone TEXT,

    email TEXT,

    status TEXT DEFAULT 'Pending'

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS packages (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    hotel TEXT,

    duration TEXT,

    transport TEXT,

    visa TEXT,

    price TEXT,

    image TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password TEXT
)
""")

cursor.execute("""
INSERT OR IGNORE INTO admins
(username, password)

VALUES
(?, ?)
""",
("admin", generate_password_hash("1234")))

connection.commit()

connection.close()

print("Database Created Successfully")
