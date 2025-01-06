import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, get_flashed_messages, url_for
from flask_session import Session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from datetime import datetime

from helpers import login_required, apology

# Configure application
app = Flask(__name__)

# Adicionar esta linha
app.secret_key = 'your_secret_key_here'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///books.db")

app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Main page"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide a username", "danger")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide a password", "danger")
            return render_template("login.html")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("Invalid username and/or password", "danger")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Login successful", "success")
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("Logout successful", "success")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username", "danger")
            return redirect("/register")
        # Ensure password was submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            flash("Must provide password", "danger")
            return redirect("/register")

        # Query database for username and check if exists
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) > 0:
            flash("Username already exists", "danger")
            return redirect("/register")

        # Check if passwords doesn't match
        if request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords don't match", "danger")
            return redirect("/register")

        # Insert new member on database
        name = request.form.get("username")
        password = request.form.get("password")
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                   name, generate_password_hash(password))
        flash("Registration successful", "success")
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        # Get search parameters from URL
        search_type = request.args.get('type')
        search_query = request.args.get('query')
        
        # If no parameters, return empty results
        if not search_type or not search_query:
            return render_template('results.html', books=[])
            
        # If we have parameters, perform the search
        api_key = 'AIzaSyBgbz9IztVv6WoI71Z-P2CrwQSCVRmxRrk'
        if search_type == 'title':
            url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{search_query}&maxResults=40&key={api_key}'
        elif search_type == 'author':
            url = f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{search_query}&maxResults=40&key={api_key}'
        else:
            flash("Invalid search type", "danger")
            return redirect("/")
            
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            books = data.get('items', [])
            return render_template('results.html', books=books, search_type=search_type, search_query=search_query)
        except Exception as e:
            flash(f"Error fetching books: {str(e)}", "danger")
            return redirect("/")
            
    # Handle POST request
    search_type = request.form.get('type')
    search_query = request.form.get('query')
    
    # Redirect to GET with parameters
    return redirect(url_for('search', type=search_type, query=search_query))


@app.route('/book/<string:book_id>')
def book_details(book_id):
    """Fetch book details from the Google Books API"""
    api_key = 'AIzaSyBgbz9IztVv6WoI71Z-P2CrwQSCVRmxRrk'
    url = f'https://www.googleapis.com/books/v1/volumes/{book_id}?key={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return render_template('book.html', book=data)
    else:
        return apology("Book not found", 404)


@app.route('/shelfs', methods=['GET'])
@login_required
def shelfs():
    status = request.args.get("status", 1, type=int)

    status_map = {
        1: "reading",
        2: "to_read",
        3: "read",
        4: "dropped"
    }
    status_text = status_map.get(status, "reading")

    try:
        query = """
            SELECT book_id
            FROM user_shelves
            WHERE user_id = ? AND status = ?
            ORDER BY added_at DESC
        """
        book_ids = db.execute(query, session["user_id"], status_text)

        books = []
        api_key = 'AIzaSyBgbz9IztVv6WoI71Z-P2CrwQSCVRmxRrk'
        
        for book in book_ids:
            book_id = book["book_id"]
            
            if not book_id:
                continue
                
            url = f'https://www.googleapis.com/books/v1/volumes/{book_id}?key={api_key}'
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                books.append(data)
            except Exception as e:
                flash(f"Error fetching book {book_id}: {str(e)}", "warning")
                continue

        return render_template('shelfs.html', books=books, status=status)
    except Exception as e:
        flash(f"Error loading shelf: {str(e)}", "danger")
        return redirect("/")


@app.route('/add-to-shelf', methods=['POST'])
@login_required
def add_to_shelf():
    status = request.form.get('status')
    book_id = request.form.get('book_id')
    redirect_url = request.form.get('redirect_url', '/shelfs')
    print(redirect_url)
    # Check if book is already on shelf
    duplicated = db.execute(
        "SELECT * FROM user_shelves WHERE book_id = ? AND user_id = ?", 
        book_id, 
        session["user_id"]
    )
    
    if not duplicated:
        # New book on db
        db.execute(
            "INSERT INTO user_shelves (user_id, book_id, status, added_at) VALUES (?, ?, ?, ?)",
            session["user_id"], 
            book_id, 
            status, 
            datetime.now()
        )
        flash("Book added to shelf", "success")
    else:
        # Update book on db
        db.execute(
            "UPDATE user_shelves SET status = ? WHERE book_id = ? AND user_id = ?",
            status,
            book_id,
            session["user_id"]
        )
        flash("Book status updated", "success")
    
    return redirect(redirect_url)


@app.route('/remove-from-shelf/<string:book_id>', methods=['POST'])
@login_required
def remove_from_shelf(book_id):
    redirect_url = request.form.get('redirect_url', '/shelfs')
    
    try:
        db.execute(
            "DELETE from user_shelves WHERE book_id = ? AND user_id = ?",
            book_id, 
            session["user_id"]
        )
        flash("Book removed from shelf", "success")
    except Exception as e:
        flash("Error removing book from shelf", "danger")
    
    return redirect(redirect_url)


@app.route('/test', methods=['POST'])
def test():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

