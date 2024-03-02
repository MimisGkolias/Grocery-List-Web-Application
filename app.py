import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, contains_number

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final-project.db")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide password", 400)

        password = request.form.get("password")
        if not contains_number(password):
            return apology("Password must contain at least one number")

        confirmation = request.form.get("confirmation")
        if confirmation != password:
            return apology("Passwords don't match")

        username = request.form.get("username")
        exists = db.execute("SELECT username from users WHERE username = ?;", username)
        if exists:
            return apology("Username already exists")

        # Query database for username
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/")
@login_required
def index():
    """Show the latest grocery list"""
    list_exists = db.execute("SELECT * from lists WHERE user_id = ?;", session['user_id'])
    if not list_exists:
        return render_template("welcome.html")

    elif list_exists:
        latest_items = []
        latest_timestamp = db.execute("SELECT MAX(timestamp) AS max_timestamp from lists WHERE user_id = ?;", session['user_id'])
        latest_timestamp = latest_timestamp[0]['max_timestamp']
        latest_list = db.execute("SELECT * from lists WHERE user_id = ? AND timestamp = ?;", session['user_id'], latest_timestamp)
        # print(latest_list[0]['id'])
        latest_items = db.execute("SELECT name from items WHERE list_id = ?;", latest_list[0]['id'])
        datetime_object = datetime.strptime(latest_timestamp, "%Y-%m-%d %H:%M:%S")
        formatted_timestamp = datetime_object.strftime("%d / %m")

        return render_template("index.html", latest_items=latest_items, formatted_timestamp=formatted_timestamp)



@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    """Creates new grocery list"""
    if request.method == "POST":
        action = request.form['action']
        items = []
        now = datetime.now()
        db.execute("INSERT INTO lists (user_id, timestamp) VALUES (?, ?);", session['user_id'], now)
        list_id_result = db.execute("SELECT last_insert_rowid();")
        list_id = list_id_result[0]['last_insert_rowid()']
        for i in range(len(request.form)):
            item = request.form.get("item" + str(i))
            if item is not None:
                items.append(item)
                db.execute("INSERT INTO items (name, list_id) VALUES (?, ?);", item, list_id)

        # print(items)


        if action == 'redirect':
            return render_template("new_list.html", items=items)
        elif action == 'add':
            return render_template("new.html")
    else:
        return render_template("new.html")


@app.route("/history")
@login_required
def history():
    """Show history of grocery lists"""
    items_list = {}
    lists = db.execute("SELECT * from lists WHERE user_id = ?;", session['user_id'])
    lists.reverse()
    # print(lists)
    # print(list_ids[0]['id'])
    # list_ids = list_ids['id']
    for list in lists:
        datetime_object = datetime.strptime(list['timestamp'], "%Y-%m-%d %H:%M:%S")
        formatted_timestamp = datetime_object.strftime("%d / %m")
        list['timestamp'] = formatted_timestamp
        list_id = list['id']
        items = db.execute("SELECT name from items WHERE list_id = ?;", list_id)
        items_list.setdefault(list_id, [])
        for item in items:
            items_list[list_id].append(item)
        # print(items_list)


    return render_template("history.html", lists=lists, items_list=items_list)
