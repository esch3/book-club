import os, csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

key = 'oqRS1g5qm2egbefRbPB6Q'
secret = '6xbgAO8Cn3QZMZHDb4EPqxukqa4UGElG06ip25ZbOo'

engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

# users, books, and reviews table for psql database
tables = {
    'users' : "CREATE TABLE users ( \
        user_id SERIAL PRIMARY KEY, \
        name VARCHAR NOT NULL, \
        password VARCHAR NOT NULL \
        );",

    'books' : "CREATE TABLE books ( \
        book_id SERIAL PRIMARY KEY, \
        isbn TEXT NOT NULL, \
        title TEXT NOT NULL, \
        author VARCHAR NOT NULL, \
        year VARCHAR NOT NULL, \
        review_count INTEGER, \
        average_rating VARCHAR \
        );",

    'reviews' : "CREATE TABLE reviews ( \
        review_id INTEGER REFERENCES users(user_id), \
        isbn INTEGER REFERENCES books(book_id), \
        review TEXT \
        );"}

def main():
    print("WARNING!!! THIS WILL DESTROY EXISTING DATABASE AND ANY EXISTING DATA")
    response = input("Do you wish to continue? [y] yes | [n] no\n")
    if response in ('n', 'no', 'N', 'NO'):
        return 0
    # initialize database and create tables
    db.execute(f"DROP TABLE IF EXISTS {'reviews'};")
    db.execute(f"DROP TABLE IF EXISTS {'users'};")
    db.execute(f"DROP TABLE IF EXISTS {'books'};")
    for item in tables:
        db.execute(f'{tables[item]}')
        db.commit()

    # read in books.csv and import into database, and commit to db
    # @@@ TODO: allow user to enter path to csv file to load data from @@@ #
    with open('books.csv', newline='') as csvfile:
        full_book_list = csv.reader(csvfile)
        header = next(full_book_list)
        count = 0
        row_count = 0
        for row in full_book_list:
            print('importing row ', row_count)
            row_count += 1
            db.execute(
                "INSERT INTO books (isbn, title, author, year) \
                VALUES (:isbn, :title, :author, :year)",
                {
                    'isbn': row[0], 
                    'title': row[1], 
                    'author': row[2], 
                    'year': row[3]
                }
            )
    db.commit()
    print("db import complete")

if __name__ == '__main__':
    main()