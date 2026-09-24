from database import get_connection

#Helper Functions

def get_bookings(search=None):

    connection = get_connection()
    cursor = connection.cursor()

    if search:

        cursor.execute("""
        SELECT * FROM bookings
        WHERE full_name LIKE %s
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
    WHERE id = %s
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
    (%s, %s, %s, %s, %s, %s)

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
    SET package = %s,
        departure_city = %s,
        travel_date = %s,
        full_name = %s,
        phone = %s,
        email = %s
    WHERE id = %s
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
    SET status = %s
    WHERE id = %s
    """, (new_status, booking_id))

    connection.commit()
    connection.close()

def delete_booking(booking_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM bookings
    WHERE id = %s
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
    WHERE id=%s
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
    WHERE category = %s
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
    WHERE username = %s
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
    (%s, %s, %s, %s, %s, %s, %s, %s)
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
    name=%s,
    hotel=%s,
    duration=%s,
    transport=%s,
    visa=%s,
    price=%s,
    image=%s,
    category=%s
    WHERE id=%s
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
    WHERE id = %s
    """, (package_id,))

    connection.commit()
    connection.close()


