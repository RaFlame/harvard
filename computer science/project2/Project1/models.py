from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String(30), primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    author = db.Column(db.String(32), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

class User(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.String(128), primary_key = True)
    password = db.Column(db.String(256), nullable = False)

    def __init__(self, userid, password):
        self.userid = userid
        self.password = password

class UserReview(db.Model):
    __tablename__ = 'UserReviews'
    r_id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(128), nullable = False)
    isbn = db.Column(db.String(30), nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    review = db.Column(db.String(256), nullable = False)

    def __init__(self, userid, isbn, rating, review):
        self.userid = userid
        self.isbn = isbn
        self.rating = rating
        self.review = review
        

