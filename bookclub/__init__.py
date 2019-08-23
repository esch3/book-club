import os, json, requests

from flask import (
    Flask, render_template, session, request, redirect, url_for, jsonify, abort
)
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
Session(app)

engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

# key for Goodread API
key = 'oqRS1g5qm2egbefRbPB6Q'
secret = '6xbgAO8Cn3QZMZHDb4EPqxukqa4UGElG06ip25ZbOo'

# books page
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('books'))
    return redirect(url_for('register'))

# register page
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        # make sure username and password fields are filled in, and user is not already in database
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute('SELECT user_id FROM users WHERE name = :username',
                        {'username': username}).rowcount != 0:
            error = f'User {username} is already registered.'
        # if successful, go to login page
        if error is None:
            db.execute('INSERT INTO users (name, password) VALUES (:username, :password)',
                       {'username': username, 'password': generate_password_hash(password)})
            db.commit()
            return redirect(url_for('login'))

    return render_template('register.html', message=error)

# login page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    # get credentials
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        user = db.execute('SELECT * FROM users WHERE name = :username',
                          {'username': username}).fetchone()
        # validate credentials
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
    # log user in if credentials checkout, clear previous session and begin new session
        if error is None:
            session.clear()
            session['user_id'] = user['user_id']
            session['name'] = username
            return redirect(url_for('search'))

    return render_template('login.html', message=error)

# logout
@app.route('/logout')
def logout():
    # log out of app - stop sqlalchemy engine, clear session data and redirect user to login page
    db.close()
    session.clear()
    return redirect(url_for('login'))

# main page, search for books
@app.route('/books', methods=["GET", "POST"])
def search():
    msg = f"You are logged in as {session['name']}"

    if request.method == 'POST':
        query = request.form.get('query')
        result = None
        reviews = None
        # check if query is an empty string, if so display "Not found"
        if query == '':
            return render_template('books.html', books=result, message=msg)
        # add wildcard for simliar search results to query
        query += '%'
        result = db.execute(
            "SELECT DISTINCT * FROM books WHERE LOWER(author) \
            LIKE LOWER(:query) OR LOWER(title) LIKE LOWER(:query) \
            OR LOWER(isbn) LIKE LOWER(:query);"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            , {
                'query': query
            }).fetchall()
        # check if query result contains any books
        if len(result) == 0:
            result = None
            return render_template('books.html', books=result, message=msg)
        # check if query is an exact match, if so redirect to reviews page
        elif len(result) == 1:
            book_id = result[0][0]
            return redirect(url_for('review', book_id=book_id))
        # display list of all possible matches
        else:
            msg = f"{session['name']}, did you mean?"
            return render_template('books.html', books=result, message=msg)

    return render_template('books.html', message=msg)

# book review page
@app.route('/review/<book_id>', methods=["GET", "POST"])
def review(book_id):
    msg = f"You are logged in as {session['name']}"
    book = db.execute("SELECT * FROM books WHERE book_id = :book_id", {
        "book_id": book_id
    }).fetchone()
    # inital values set to in case JSON request throws an error
    work_ratings_count = 0
    average_rating = '0'
    # if link to book is followed from search page via "GET"
    if request.method == 'GET':
        print("GET REQUEST: ", book_id)
        # goodreads API to get ratings_count and average_rating for reviews table
        try:
            res = requests.get(
                "https://www.goodreads.com/book/review_counts.json",
                params={
                "key": key,
                "isbns": book[1]
            })
            work_ratings_count = res.json()['books'][0]['work_ratings_count']
            average_rating = res.json()['books'][0]['average_rating']
        except json.JSONDecodeError as err:
            print(err)
        # get updated book with review_count, and ratings
        db.execute(
            "UPDATE books SET review_count = :review_count, average_rating = :average_rating WHERE book_id=:book_id",
            {"review_count": work_ratings_count, "average_rating": average_rating, "book_id": book_id}
            )
        db.commit()
        book = db.execute("SELECT * FROM books WHERE book_id = :book_id", {
            "book_id": book_id
            }).fetchone()
        reviews = db.execute(
            "SELECT review, name, rating FROM reviews JOIN users ON \
            (reviews.review_id = users.user_id) WHERE isbn = :book_id"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      , {
            "book_id": book_id
            }).fetchall()
        return render_template('review.html', reviews=reviews, book=book, message=msg)

    # handles user review submission
    if request.method == 'POST':
        review = request.form.get('review')
        rating = request.form.get('rating')
        print(rating)
        if review is not None:
            # check to see if user already posted a review
            if db.execute("SELECT review_id, isbn FROM reviews WHERE review_id = :user_id AND isbn = :book_id",
                {"user_id": session["user_id"], "book_id": book_id}).rowcount != 0:
                return render_template(
                    'books.html',
                    message=
                    f'Sorry {session["name"]}. You have already posted a review for this book. \
                        Try searching for another book.'
                )
            else:
                db.execute("INSERT INTO reviews (review_id, isbn, review, rating) \
                    VALUES (:review_id, :isbn, :review, :rating)"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 ,
                    {"review_id": session['user_id'], "isbn": book_id, "review": review, "rating": rating})
                db.commit()

    return redirect(url_for('review', book_id=book_id))
    #return render_template('review.html', message=f'Thank you {session["name"]}. Your review posted.')

# error handler for API call
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

# make API call to /api/<isbn>
@app.route('/api/<isbn>', methods=["GET"])
def json_response(isbn):
    work_ratings_count = 0
    average_rating = '0'
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn",
    {"isbn": isbn}).fetchone()
    if book is None:
        abort(404, description="Resource not found")

    # if book not found, return empty JSON book object
    '''
    if book is None:
        d = {
            "title": None,
            "author": None,
            "year": None,
            "isbn": isbn,
            "review_count": None,
            "average_score": None
        }
        return jsonify(d)
    '''
    # try to update book object with review count and ratings from Goodread's API
    try:
        res = requests.get(
            "https://www.goodreads.com/book/review_counts.json",
            params={
            "key": key,
            "isbns": book[1]
        })
        work_ratings_count = res.json()['books'][0]['work_ratings_count']
        average_rating = res.json()['books'][0]['average_rating']
    except json.JSONDecodeError as err:
        print(err)
    db.execute(
        "UPDATE books SET review_count=:review_count, average_rating=:average_rating WHERE isbn=:isbn",
        {"review_count": work_ratings_count, "average_rating": average_rating, "isbn": isbn }
        )
    db.commit()
    # get updated book with review count and ratings
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {
        "isbn": isbn
        }).fetchone()
    # prep book object to be jsonified
    d = dict(book.items())
    return jsonify(d)