from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = "Banana&Applesin1999"

def auth_user():
    connection = pymysql.connect(
            host='localhost',
            user='client',
            password='!Passw0rd?',
            database='greenstore'
        )
    cursor = connection.cursor()
    return cursor, connection

@app.route("/")
def home():
    return render_template("home.html", title="Green Store - Home", header="Welcome to Green Store")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cursor, connection = auth_user()
        username = request.form["username"]
        password = request.form["password"]

        # Check if the user exists
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            flash(f"Welcome back, {username}!", "success")
            return redirect("/")
        else:
            flash("Invalid username or password. Please try again.", "error")
            return redirect("/login")
    return render_template("login.html", title="Green Store - Login", header="Login to Green Store")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        cursor, connection = auth_user()
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Check if the user already exists
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash("Username already taken. Please choose another one.", "error")
            return redirect("/signup")
        
        # Add user registration logic
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, password))
        connection.commit()
        connection.close()

        flash("Account created successfully! Please log in.", "success")
        return redirect("/login")
    return render_template("signup.html", title="Green Store - Signup", header="Join Green Store")


if __name__ == "__main__":
    app.run(debug=True)
