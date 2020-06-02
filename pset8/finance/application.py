import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd, search, total_net_worth


# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        # Gets data from the user according database ID

        # Gets username
        username = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
        # Gets the user cash
        user_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        user_cash = user_cash[0]["cash"]

        # Gets users shares, symbol and total ammount and using the search function, updates price and total value
        user_stocks = db.execute(
            "SELECT symbol, SUM(quantity) FROM portfolio WHERE id = :id GROUP BY symbol", id=session["user_id"])
        search(user_stocks)

        return render_template("index.html", username=username[0]["username"], user_stocks=user_stocks, user_cash=user_cash,
                               total_net_worth=total_net_worth(user_stocks, user_cash))

    else:
        try:
            new_cash = int(request.form.get("newcash"))
        except ValueError:
            return apology("Must input only numbers", 400)
        if not new_cash:
            return apology("Must input a number", 400)
        user_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        user_cash = user_cash[0]["cash"]
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", id=session["user_id"], cash=user_cash + new_cash)
        return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:

        # Gets data from the forms
        try:
            symbol = request.form.get("symbol")
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Shares must be a positive number and greater than zero", 400)

        # If input is wrong, return apology
        if not symbol:
            return apology("Must input a symbol", 400)
        if not lookup(symbol):
            return apology("Incorrect symbol", 400)
        if shares <= 0:
            return apology("Shares must be a positive number and greater than zero", 400)

        # Saves input

        symbol_dict = lookup(symbol)
        user_will_purchase = int(symbol_dict.get("price") * shares)
        user_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        user_cash = int(user_cash[0]["cash"])

        # checks account balance, else returns an apology
        if user_cash < user_will_purchase:
            return apology("Not enough money to make the purchase!", 403)

        # If account balance has sufficient funds..
        else:

            # Saves correspondant data in portfolio table inside finance
            db.execute("INSERT INTO portfolio (id, symbol, quantity, price, date) VALUES (:id, :symbol, :quantity, :price, :date)",
                       id=session["user_id"], symbol=symbol_dict.get("symbol"), quantity=shares, price=symbol_dict.get("price"), date=datetime.now())

            # Updates finance db in users table
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=user_cash - user_will_purchase, id=session["user_id"])
        return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    user = db.execute("SELECT * FROM users WHERE username = :username", username=username)
    if user or username == "":
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    data = db.execute("SELECT symbol, quantity, price, date FROM portfolio WHERE id = :id", id=session["user_id"])
    return render_template("history.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # When form is submitted, POST
    if request.method == "POST":

        # Check form for correct username input
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Check form for correct password input
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Check correctness of username and password
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember what user is logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # If passed with GET then render login template
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        if not lookup(symbol):
            return apology("Symbol not found", 400)
        else:
            symbol_dict = lookup(symbol)
            print(symbol_dict)
            return render_template("quoted.html", company=symbol_dict.get("name"), price=symbol_dict.get("price"), symbol=symbol_dict.get("symbol"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Get the username and password from the HTML forms in register.html
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":

        # Get data form the user for register
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        check_username = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        # Ensures proper usage

        if check_username:
            return apology("Username already exists", 400)
        elif not username:
            return apology("Missing username", 400)
        elif not password:
            return apology("Missing password", 400)
        elif not confirmation:
            return apology("Missing confirmation password", 400)
        elif password != confirmation:
            return apology("Passwords don't match!", 400)

        if password:
            if not any(x.isupper() for x in password):
                return apology("Password format incorrect", 400)
            elif not any(x.islower() for x in password):
                return apology("Password format incorrect", 400)
            elif not any(x.isdigit() for x in password):
                return apology("Password format incorrect", 400)
            elif len(password) < 4:
                return apology("Password format incorrect", 400)

        # Hashes the password for storage
        password_hash = generate_password_hash(password)

        # Stores the username and a hashed password in the 'user' table form the finance database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                   username=request.form.get("username"), hash=password_hash)

        # Stores user id to keep session
        user_id = db.execute("SELECT id FROM users WHERE username = :username AND hash = :hash",
                             username=request.form.get("username"), hash=password_hash)
        session["user_id"] = user_id[0]["id"]

        # Redirects to index
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        stocks_avaliable = db.execute("SELECT symbol FROM portfolio WHERE id = :id GROUP BY symbol HAVING SUM(quantity) > 0",
                                      id=session["user_id"])
        print(stocks_avaliable)
        return render_template("sell.html", stocks_avaliable=stocks_avaliable)
    else:
        symbol = (request.form.get("symbol")).upper()
        ammount_user_wants_to_sell = int(request.form.get("shares"))

        # Makes sure user gives correct amount
        if ammount_user_wants_to_sell <= 0:
            return apology("You must input a number greater than zero", 400)
        if not lookup(symbol):
            return apology("Incorrect symbol", 400)

        # Checks inputed stock of the user and return the amount he owns
        user_stocks = db.execute("SELECT SUM(quantity) FROM portfolio WHERE id = :id AND symbol = :symbol",
                                 id=session["user_id"], symbol=symbol)
        if user_stocks[0]["SUM(quantity)"] == None or user_stocks[0]["SUM(quantity)"] == 0:
            return apology("User doesn't own that stock", 400)

        # Makes sure the user has sufficient ammount to sell
        if user_stocks[0]["SUM(quantity)"] < ammount_user_wants_to_sell:
            return apology("You are trying to sell more than you own", 400)

        # Updates database with the new ammount of shares and sale profit

        # Updates users current cash according to the ammount profit after the transaction
        total_sell = (lookup(symbol)).get("price") * ammount_user_wants_to_sell
        users_current_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        users_current_cash = users_current_cash[0]["cash"]
        db.execute("UPDATE users SET cash = :cash WHERE id = :id",
                   id=session["user_id"], cash=float(users_current_cash) + float(total_sell))

        # Updates the ammount of stocks
        db.execute("INSERT INTO portfolio (id, symbol, quantity, price, date) VALUES (:id, :symbol, :quantity, :price, :date)",
                   id=session["user_id"], symbol=symbol, quantity=-(ammount_user_wants_to_sell), price=(lookup(symbol)).get("price"),
                   date=datetime.now())

        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


@app.route("/change", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "GET":
        return render_template("change.html")
    else:
        # Get the required data
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensures proper usage
        if password:
            if not any(x.isupper() for x in password):
                return apology("Password format incorrect", 400)
            elif not any(x.islower() for x in password):
                return apology("Password format incorrect", 400)
            elif not any(x.isdigit() for x in password):
                return apology("Password format incorrect", 400)
            elif len(password) < 4:
                return apology("Password format incorrect", 400)

        if not password:
            return apology("Missing password", 400)

        if not confirmation:
            return apology("Missing confirmation password", 400)

        if password != confirmation:
            return apology("Passwords don't match", 400)



        # Hash password for storage
        password_hash = generate_password_hash(password)

        # Stores username and a hashed password in the user table form in finance database
        db.execute("UPDATE users SET hash = :password WHERE id = :id", password=password_hash, id=session["user_id"])

        # Redirects to the index
        return redirect("/")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)