import psycopg
import os
from werkzeug.security import generate_password_hash

connection = psycopg.connect(os.environ["DATABASE_URL"])
cursor = connection.cursor()

cursor.execute("""
INSERT INTO admins (username, password)
VALUES (%s, %s)
ON CONFLICT (username) DO NOTHING
""",
(
    "admin",
    generate_password_hash("1234")
))

connection.commit()
connection.close()

print("Admin account initialized successfully")