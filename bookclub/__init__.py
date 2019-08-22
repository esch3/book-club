import os

from flask import Flask, render_template, session, request, redirect, url_for
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

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute('SELECT user_id FROM users WHERE name = :username',
                        {'username': username}).rowcount != 0:
            error = f'User {username} is already registered.'

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

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        user = db.execute('SELECT * FROM users WHERE name = :username',
                          {'username': username}).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['user_id']
            session['name'] = username
            return redirect(url_for('books'))

    return render_template('login.html', message=error)

# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# main page
@app.route('/books', methods=["GET", "POST"])
def books():
    msg = f"You are logged in as {session['name']}"
    if request.method == 'POST':
        title = request.form.get('title')
        book = None
        book = db.execute(
            "SELECT * FROM books WHERE title = :title", {'title': title}).fetchone()
        if book is not None:
            print(book)
            return render_template('books.html', book=book, message=msg)
        else:
            book = ('Not found')
            print(book)
            return render_template('books.html', book=book, message=msg)

    return render_template('books.html', message=msg)