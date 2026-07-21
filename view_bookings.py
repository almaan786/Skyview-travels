import sqlite3

connection = sqlite3.connect("bookings.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM bookings")

rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()
