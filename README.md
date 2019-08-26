# Bookclub
An app that allows users to read and create book reviews.

# Motivation
The motivation for building this project is give the user an easy to use, front end to a database that contains over 5000 popular books, along with their average rating and any reviews left on the app by users of Bookclub.

# Build status
Version 1.0

# Tech/Framework used
This project is coded in Python, using Flask microframework as web service, Postgresql via Heroku on the back end, and Bootstrap on the front end.

# Installation
This installation method is a demo on how to hit the ground running and serve external clients on port 80 for motivation. 
1. <a href="https://aws.amazon.com/ec2/getting-started/">Spin up an EC2 Ubuntu Server.</a> 
2. Configure security group to allow hosts on 80.
3. Log into ubuntu server.
4. Type the following commands.

$ sudo apt update  
$ sudo apt install python3-pip  
$ git clone https://github.com/tomeschnyc/book-club.git  
$ cd book-club   
$ sudo pip3 install -e .  
$ sudo flask run  
  
5. Type the DNS or IP of your instance into your browser and check out the Bookclub!

There is also a database import program found in 'import.py', that imports the database schema to Heroku, and loads the book data found in 'books.csv' into the database. This is for educational purposes only as it is separate from the app itself, and has already been ran, but is included because it is a necessary dependency of the app. If you wish to utilize your own database, set your 'DATABASE_URL' environment variable to your own database before running 'import.'


# API Reference
<a href="https://www.goodreads.com/api">Goodreads API</a> is implemented in order to get number of ratings and average rating, to give the reader a quick idea of how popular a given book is. Bookclub also has an API of it's own which can be found by following the '/api/<isbn>' URL. 

# How to use
1. Register as a new user
2. User will be redirected to the login page.
3. Login.
4. Enter title, author or ISBN of a book. If an exact match is not found, the search will return a list of results of matches that are similar to the search query. If an exact match is found, the user will be routed directly to that book.
5. The user can then follow a link to a book's page, where the book's title, author, ISBN, year of publication, number of ratings, and average rating are displayed. 
6. Reviews are also displayed, and the user has the option of leaving at most one review and rating. 
7. The user can then either search for another book, or logout of the app.
8. Developer's can access the Bookclub API by following the '/api/<isbn>', where book info will be returned in JSON format or a 404 error if the book is not found.

# Contribute
You can contribute to the page or add resources by following these <a href="https://github.com/zulip/zulip-electron/blob/master/CONTRIBUTING.md">contributing guideline</a>. Thanks!
  
# Credits
@author: Tom Esch

 
