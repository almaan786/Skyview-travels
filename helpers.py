from database import get_connection
import os
import requests

#Helper Functions

def get_bookings(search=None):

    connection = get_connection()
    cursor = connection.cursor()

    if search:

        cursor.execute("""
        SELECT * FROM bookings
        WHERE full_name LIKE ?
        """, ('%' + search + '%',))

    else:

        cursor.execute("""
        SELECT * FROM bookings
        """)

    bookings = cursor.fetchall()

    connection.close()

    return bookings


def get_booking_by_id(booking_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM bookings
    WHERE id = ?
    """, (booking_id,))

    booking = cursor.fetchone()

    connection.close()

    return booking


def create_booking(package,
                   departure_city,
                   travel_date,
                   full_name,
                   phone,
                   email):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO bookings
    (package,
    departure_city,
    travel_date,
    full_name,
    phone,
    email)

    VALUES
    (?, ?, ?, ?, ?, ?)

    RETURNING id
    """,
    (
        package,
        departure_city,
        travel_date,
        full_name,
        phone,
        email
    ))

    booking_id=cursor.fetchone()[0]

    connection.commit()
    connection.close()

    return booking_id

def update_booking(
    booking_id,
    package,
    departure_city,
    travel_date,
    full_name,
    phone,
    email
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE bookings
    SET package = ?,
        departure_city = ?,
        travel_date = ?,
        full_name = ?,
        phone = ?,
        email = ?
    WHERE id = ?
    """, (
        package,
        departure_city,
        travel_date,
        full_name,
        phone,
        email,
        booking_id
    ))

    connection.commit()
    connection.close()

def update_booking_status(booking_id, new_status):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE bookings
    SET status = ?
    WHERE id = ?
    """, (new_status, booking_id))

    connection.commit()
    connection.close()

def delete_booking(booking_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM bookings
    WHERE id = ?
    """, (booking_id,))

    connection.commit()
    connection.close()

def get_package_by_id(package_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
    """
    SELECT id, name, hotel, duration, transport, visa, price, image, category
    FROM packages
    WHERE id=?
    """,
    (package_id,))

    package = cursor.fetchone()

    connection.close()

    return package

def get_packages(category=None):
    connection = get_connection()
    cursor = connection.cursor()

    if category :
        cursor.execute( """
    SELECT id, name, hotel, duration, transport, visa, price, image, category
    FROM packages
    WHERE category = ?
    """,
    (category,))

    else :
        cursor.execute("""
    SELECT id, name, hotel, duration, transport, visa, price, image, category
    FROM packages
    """)

    packages = cursor.fetchall()
    connection.close()

    return packages

def get_admin_by_username(username):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM admins
    WHERE username = ?
    """, (username,))

    admin = cursor.fetchone()

    connection.close()

    return admin


def create_package(
    name,
    category,
    hotel,
    duration,
    transport,
    visa,
    price,
    image
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO packages
    (name, hotel, duration, transport, visa, price, image, category)

    VALUES
    (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        name,
        hotel,
        duration,
        transport,
        visa,
        price,
        image,
        category
    ))

    connection.commit()
    connection.close()

def update_package(
    package_id,
    name,
    category,
    hotel,
    duration,
    transport,
    visa,
    price,
    image
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE packages
    SET
    name=?,
    hotel=?,
    duration=?,
    transport=?,
    visa=?,
    price=?,
    image=?,
    category=?
    WHERE id=?
    """,
    (
        name,
        hotel,
        duration,
        transport,
        visa,
        price,
        image,
        category,
        package_id
    ))

    connection.commit()
    connection.close()

def delete_package(package_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM packages
    WHERE id = ?
    """, (package_id,))

    connection.commit()
    connection.close()

def send_whatsapp_notification(booking_id, customer_name, package_name):

    token = os.environ["WHATSAPP_TOKEN"]

    phone_number_id = "1303844576142865"
    recipient = "918260889678"

    url = f"https://graph.facebook.com/v26.0/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "template",
        "template": {
            "name": "booking_notification",
            "language": {
                "code": "en"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": str(booking_id)
                        },
                        {
                            "type": "text",
                            "text": customer_name
                        },
                        {
                            "type": "text",
                            "text": package_name
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    return response
