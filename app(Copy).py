from flask import Flask, render_template, request,redirect,session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

app.secret_key = "4dcbf82c1ab1c5f0f4d9b3f6f7f7a8c24ea18e6d1d7a5d2f5d7b2e0a4f0c8a9b"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/book", methods=["GET", "POST"])
def book():

    selected_package = request.args.get("package")
    
    print(selected_package)

    if request.method == "POST":
        
        package = request.form["package"]
        departure_city = request.form["departure_city"]
        travel_date = request.form["travel_date"]
        full_name = request.form["full_name"]
        phone = request.form["phone"]
        email = request.form["email"]

        connection = sqlite3.connect("bookings.db")

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
        """,
        (
        package,
        departure_city,
        travel_date,
        full_name,
        phone,
        email
        ))

        connection.commit()

        connection.close()

        return render_template("confirmation.html")

    connection = sqlite3.connect("bookings.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM packages")

    packages = cursor.fetchall()

    connection.close()

    return render_template(
    "book.html",
    packages=packages,
    selected_package=selected_package
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = sqlite3.connect("bookings.db")

        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM admins
        WHERE username = ?
        """, (username,))

        admin = cursor.fetchone()

        connection.close()

        if admin and check_password_hash(admin[2], password):

            session["admin"] = True

            return redirect("/admin")

        return "Invalid username or password"

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/login")

@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect("/login")

    search = request.args.get("search")

    connection = sqlite3.connect("bookings.db")

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

    return render_template("admin.html",
                           bookings=bookings)

@app.route("/update_status/<int:booking_id>/<new_status>")
def update_status(booking_id, new_status):

    if "admin" not in session:
        return redirect("/login")

    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE bookings
    SET status = ?
    WHERE id = ?
    """, (new_status, booking_id))

    connection.commit()
    connection.close()

    return redirect("/admin")

@app.route("/confirm_delete/<int:booking_id>")
def confirm_delete(booking_id):

    if "admin" not in session:
        return redirect("/login")

    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM bookings
    WHERE id = ?
    """, (booking_id,))

    booking = cursor.fetchone()

    connection.close()

    return render_template(
        "confirm_delete.html",
        booking=booking
    )

@app.route("/delete_booking/<int:booking_id>")
def delete_booking(booking_id):

    if "admin" not in session:
        return redirect("/login")

    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM bookings
    WHERE id = ?
    """, (booking_id,))

    connection.commit()
    connection.close()

    return redirect("/admin")

@app.route("/edit_booking/<int:booking_id>", methods=["GET", "POST"])
def edit_booking(booking_id):

    if "admin" not in session:
        return redirect("/login")

    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    if request.method == "POST":

        package = request.form["package"]
        departure_city = request.form["departure_city"]
        travel_date = request.form["travel_date"]
        full_name = request.form["full_name"]
        phone = request.form["phone"]
        email = request.form["email"]

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

        return redirect("/admin")

    cursor.execute("""
    SELECT * FROM bookings
    WHERE id = ?
    """, (booking_id,))

    booking = cursor.fetchone()

    connection.close()

    return render_template(
        "edit_booking.html",
        booking=booking
    )

@app.route("/umrah")
def umrah():

    connection = sqlite3.connect("bookings.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM packages")

    packages = cursor.fetchall()

    connection.close()

    return render_template(
        "umrah.html",
        packages=packages
    )

@app.route("/hajj")
def hajj():
    return "<h1>Hajj Packages - Coming Soon</h1>"

@app.route("/flights")
def flights():
    return "<h1>International Flights - Coming Soon</h1>"

@app.route("/tours")
def tours():
    return "<h1>Tour Packages - Coming Soon</h1>"

@app.route("/offers")
def offers():
    return "<h1>Special Offers - Coming Soon</h1>"

@app.route("/admin/packages")
def admin_packages():

    if "admin" not in session:
        return redirect("/login")

    connection = sqlite3.connect("bookings.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM packages")

    packages = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_packages.html",
        packages=packages
    )


@app.route("/add_package", methods=["GET", "POST"])
def add_package():

    if "admin" not in session:
        return redirect("/login")

    if request.method == "POST":

        name = request.form["name"]
        hotel = request.form["hotel"]
        duration = request.form["duration"]
        transport = request.form["transport"]
        visa = request.form["visa"]
        price = request.form["price"]
        image = request.form["image"]

        connection = sqlite3.connect("bookings.db")

        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO packages
        (name, hotel, duration, transport, visa, price, image)

        VALUES
        (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            hotel,
            duration,
            transport,
            visa,
            price,
            image
        ))

        connection.commit()
        connection.close()

        return redirect("/admin/packages")

    return render_template("add_package.html")


@app.route("/edit_package/<int:package_id>", methods=["GET", "POST"])
def edit_package(package_id):

    if "admin" not in session:
        return redirect("/login")

    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    if request.method == "POST":

        name = request.form["name"]
        hotel = request.form["hotel"]
        duration = request.form["duration"]
        transport = request.form["transport"]
        visa = request.form["visa"]
        price = request.form["price"]
        image = request.form["image"]

        cursor.execute("""
        UPDATE packages

        SET
        name=?,
        hotel=?,
        duration=?,
        transport=?,
        visa=?,
        price=?,
        image=?

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
            package_id
        ))

        connection.commit()
        connection.close()

        return redirect("/admin/packages")

    cursor.execute(
        "SELECT * FROM packages WHERE id=?",
        (package_id,)
    )

    package = cursor.fetchone()

    connection.close()

    return render_template(
        "edit_package.html",
        package=package
    )


@app.route("/confirm_delete_package/<int:package_id>")
def confirm_delete_package(package_id):

    if "admin" not in session:
        return redirect("/login")

    connection = sqlite3.connect("bookings.db")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM packages WHERE id=?",
        (package_id,)
    )

    package = cursor.fetchone()

    connection.close()

    return render_template(
        "confirm_delete_package.html",
        package=package
    )

@app.route("/delete_package/<int:package_id>")
def delete_package(package_id):

    if "admin" not in session:
        return redirect("/login")

    connection = sqlite3.connect("bookings.db")

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM packages WHERE id=?",
        (package_id,)
    )

    connection.commit()

    connection.close()

    return redirect("/admin/packages")

@app.route("/faq")
def faq():
    return "<h1>FAQ - Coming Soon</h1>"

@app.route("/contact")
def contact():
    return "<h1>Contact Us - Coming Soon</h1>"

if __name__ == "__main__":
    app.run(debug=True)
