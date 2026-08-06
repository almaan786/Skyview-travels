from flask import Flask, render_template, request,redirect,session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# Todo:- writing the helper functions 
# then replace the helper function with postgresql

app = Flask(__name__)

app.secret_key = "4dcbf82c1ab1c5f0f4d9b3f6f7f7a8c24ea18e6d1d7a5d2f5d7b2e0a4f0c8a9b"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/book", methods=["GET", "POST"])
def book():

    selected_package = request.args.get("package")
    category = request.args.get("category")

    print(selected_package)

    if request.method == "POST":

        package = request.form["package"]
        departure_city = request.form["departure_city"]
        travel_date = request.form["travel_date"]
        full_name = request.form["full_name"]
        phone = request.form["phone"]
        email = request.form["email"]

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

        return render_template("customer/confirmation.html")

    connection = get_connection()
    cursor = connection.cursor()

    if category:

        cursor.execute("""
        SELECT * FROM packages
        WHERE category = ?
        """, (category,))

    else:

        cursor.execute("SELECT * FROM packages")

    packages = cursor.fetchall()

    connection.close()

    return render_template(
        "customer/book.html",
        packages=packages,
        selected_package=selected_package
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection()

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

    return render_template("auth/login.html")

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/login")

@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect("/login")

    search = request.args.get("search")

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

    return render_template("admin/admin.html",
                           bookings=bookings)
# Booking Handling

@app.route("/update_status/<int:booking_id>/<new_status>")
def update_status(booking_id, new_status):

    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()
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

    booking=get_booking_by_id(booking_id)

    return render_template(
        "admin/confirm_delete.html",
        booking=booking
    )

@app.route("/delete_booking/<int:booking_id>")
def delete_booking(booking_id):

    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()
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

    connection = get_connection()
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

    booking = get_booking_by_id(booking_id)

    connection.close()

    return render_template(
        "admin/edit_booking.html",
        booking=booking
    )

def get_packages(category=None):
    connection = get_connection()
    cursor = connection.cursor()

    if category :
        cursor.execute(
            "SELECT * FROM packages WHERE category = ?",
            (category,)
        )

    else :
        cursor.execute("SELECT * FROM packages")
    packages = cursor.fetchall()
    connection.close()

    return packages

@app.route("/umrah")
def umrah():
    return render_template(
        "customer/umrah.html",
        packages=get_packages("Umrah")
    )

@app.route("/hajj")
def hajj():
    return render_template(
        "customer/hajj.html",
        packages=get_packages("Hajj")
    )

@app.route("/holidays")
def holidays():
    return render_template("customer/holidays.html")

@app.route("/ziyarats")
def ziyarats():
    return render_template("customer/ziyarats.html")

@app.route("/services")
def services():
    return render_template("customer/services.html")

# Travel Package Handling

@app.route("/admin/packages")
def admin_packages():

    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM packages")

    packages = cursor.fetchall()

    connection.close()

    return render_template(
        "admin/admin_packages.html",
        packages=packages
    )


@app.route("/add_package", methods=["GET", "POST"])
def add_package():

    if "admin" not in session:
        return redirect("/login")

    if request.method == "POST":

        name = request.form["name"]
        category = request.form["category"]
        hotel = request.form["hotel"]
        duration = request.form["duration"]
        transport = request.form["transport"]
        visa = request.form["visa"]
        price = request.form["price"]
        image = request.form["image"]

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO packages
        (name, hotel, duration, transport, visa, price, image,category)

        VALUES
        (?, ?, ?, ?, ?, ?, ?,?)
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

        return redirect("/admin/packages")

    return render_template("admin/add_package.html")


@app.route("/edit_package/<int:package_id>", methods=["GET", "POST"])
def edit_package(package_id):

    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        name = request.form["name"]
        category = request.form["category"]
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

        return redirect("/admin/packages")

    package = get_package_by_id(package_id)

    return render_template(
        "admin/edit_package.html",
        package=package
    )


@app.route("/confirm_delete_package/<int:package_id>")
def confirm_delete_package(package_id):

    if "admin" not in session:
        return redirect("/login")

    package = get_package_by_id(package_id)

    return render_template(
        "admin/confirm_delete_package.html",
        package=package
    )

@app.route("/delete_package/<int:package_id>")
def delete_package(package_id):

    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM packages WHERE id=?",
        (package_id,)
    )

    connection.commit()

    connection.close()

    return redirect("/admin/packages")

@app.route("/admin/questions")
def admin_questions():

    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM questions
    """)

    questions = cursor.fetchall()

    connection.close()

    return render_template(
        "admin_questions.html",
        questions=questions
    )

@app.route("/answer_question/<int:question_id>", methods=["GET", "POST"])
def answer_question(question_id):

    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        answer = request.form["answer"]

        cursor.execute("""
        UPDATE questions

        SET
        answer = ?,
        status = ?

        WHERE id = ?
        """,
        (
            answer,
            "Answered",
            question_id
        ))

        connection.commit()
        connection.close()

        return redirect("/admin/questions")

    cursor.execute("""
    SELECT * FROM questions
    WHERE id = ?
    """, (question_id,))

    question = cursor.fetchone()

    connection.close()

    return render_template(
        "answer_question.html",
        question=question
    )

@app.route("/qa", methods=["GET", "POST"])
def qa():

    if request.method == "POST":

        full_name = request.form["full_name"]
        phone = request.form["phone"]
        question = request.form["question"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO questions
        (full_name, phone, question)

        VALUES
        (?, ?, ?)
        """,
        (
            full_name,
            phone,
            question
        ))

        connection.commit()
        connection.close()

        return render_template("confirmation.html")

    return render_template("qa.html")



@app.route("/contact")
def contact():
    return render_template("customer/contact.html")

#Helper Functions

def get_connection():

    return sqlite3.connect("bookings.db")

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

def get_package_by_id(package_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM packages WHERE id=?",
        (package_id,)
    )

    package = cursor.fetchone()

    connection.close()

    return package

#

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
