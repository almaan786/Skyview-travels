from dotenv import load_dotenv

load_dotenv("local.env")

import os
from flask import Flask, render_template, request,redirect,session
from werkzeug.security import check_password_hash
from helpers import (
    get_packages,
    get_package_by_id,
    get_bookings,
    get_booking_by_id,
    get_admin_by_username,
    create_booking,
    update_booking,
    update_booking_status,
    delete_booking,
    create_package,
    update_package,
    delete_package
)


# Todo:- writing the helper functions 
# then replace the helper function with postgresql
#Todo:- You have to test the package crud operations

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

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

        booking_id = create_booking(
        package,
        departure_city,
        travel_date,
        full_name,
        phone,
        email
        )

        return render_template("customer/confirmation.html")

    packages = get_packages(category)

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

        admin = get_admin_by_username(username)

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

    bookings = get_bookings(search)

    return render_template("admin/admin.html",
                           bookings=bookings)
# Booking Handling

@app.route("/update_status/<int:booking_id>/<new_status>")
def update_status(booking_id, new_status):

    if "admin" not in session:
        return redirect("/login")

    update_booking_status(booking_id, new_status)

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
def delete_booking_route(booking_id):

    if "admin" not in session:
        return redirect("/login")

    delete_booking(booking_id)

    return redirect("/admin")

@app.route("/edit_booking/<int:booking_id>", methods=["GET", "POST"])
def edit_booking(booking_id):

    if "admin" not in session:
        return redirect("/login")


    if request.method == "POST":

        package = request.form["package"]
        departure_city = request.form["departure_city"]
        travel_date = request.form["travel_date"]
        full_name = request.form["full_name"]
        phone = request.form["phone"]
        email = request.form["email"]

        update_booking(
            booking_id,
            package,
            departure_city,
            travel_date,
            full_name,
            phone,
            email
        )

        return redirect("/admin")

    booking = get_booking_by_id(booking_id)


    return render_template(
        "admin/edit_booking.html",
        booking=booking
    )

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

    packages = get_packages()

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

        create_package(
    	    name,
    	    category,
   	    hotel,
   	    duration,
    	    transport,
    	    visa,
    	    price,
    	    image
	)

        return redirect("/admin/packages")

    return render_template("admin/add_package.html")


@app.route("/edit_package/<int:package_id>", methods=["GET", "POST"])
def edit_package(package_id):

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

        update_package(
            package_id,
            name,
            category,
            hotel,
            duration,
            transport,
            visa,
            price,
    	    image
	)

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
def delete_package_route(package_id):

    if "admin" not in session:
        return redirect("/login")

    delete_package(package_id)

    return redirect("/admin/packages")

@app.route("/contact")
def contact():
    return render_template("customer/contact.html")

@app.route("/robots.txt")
def robots():
    return """User-agent: *
Allow: /

Disallow: /admin/

Sitemap: https://skyview-travels.onrender.com/sitemap.xml
""", 200, {"Content-Type": "text/plain"}

@app.route("/sitemap.xml")
def sitemap():
    return """<?xml version="1.0" encoding="UTF-8"?>

<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

    <url>
        <loc>https://skyview-travels.onrender.com/</loc>
    </url>

    <url>
        <loc>https://skyview-travels.onrender.com/umrah</loc>
    </url>

    <url>
        <loc>https://skyview-travels.onrender.com/hajj</loc>
    </url>

    <url>
        <loc>https://skyview-travels.onrender.com/holidays</loc>
    </url>

    <url>
        <loc>https://skyview-travels.onrender.com/ziyarats</loc>
    </url>

    <url>
        <loc>https://skyview-travels.onrender.com/services</loc>
    </url>

    <url>
        <loc>https://skyview-travels.onrender.com/contact</loc>
    </url>

</urlset>
""", 200, {"Content-Type": "application/xml"}

#

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
