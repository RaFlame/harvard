import os, requests

from flask import Flask, session, render_template, url_for, redirect, g, request, redirect, jsonify
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_, and_
from models import *

app = Flask(__name__)

# Check for environment variable, API KEY, SECRET KEY
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

if not os.getenv("GOODREADS_API_KEY"):
    raise RuntimeError("GOODREADS_API_KEY is not set")

if not os.getenv("SECRET_KEY"):
    raise RuntimeError("SECRET_KEY is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
api_key = os.getenv("GOODREADS_API_KEY")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    if 'user_name' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user_name' in session:
            return redirect(url_for('index'))
        return render_template('login.html')
    else:
        
        if not request.form.get('username'):
            return render_template('login.html', errmsg='Please provide valid username')
        if not request.form.get('password'):
            return render_template('login.html', errmsg='Please provide valid password')

        user = User.query.get(request.form.get('username'))
        if user is None:
            return render_template('register.html', errmsg='No records found. Please register first')
        else:
            # success, now set session vars
            if check_password_hash(user.password, request.form.get('password')):
                session['user_name'] = user.userid
                return render_template('index.html', sucmsg='Logged in successfully')
            # display error alert
            else:
                return render_template('login.html', errmsg='Wrong password! Please try again')



@app.route('/register', methods=['GET', 'POST'])
def register():
    session.clear()
    if request.method == 'GET':
        return render_template('register.html')
    else:

        if not request.form.get('username'):
            return render_template('register.html', errmsg='Please provide valid username')
        if not request.form.get('password'):
            return render_template('register.html', errmsg='Please provide valid password')
        
        #checking if user exists
        user = User.query.get(request.form.get('username'))
        if user is not None:
            return render_template('register.html', errmsg='User already exists! Please try a different username')
        else:
            new_user = User(request.form.get('username'), generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8))
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html', sucmsg='Successfully Registered! Please login now')

@app.route('/logout')
def log_out():
    session.pop('user_name')
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    
    if not request.form.get('search'):
        return render_template('index.html', errmsg='Please provide a search query')
    else:
        st = '%{}%'.format(request.form.get('search'))
        books = Book.query.filter(or_(Book.isbn.like(st), Book.author.like(st), Book.title.like(st))).limit(9).all()

        #if not found
        if not books:
            return render_template('index.html', errmsg='No result found')
        #else display all 9 books
        return render_template('books.html', books=books)

@app.route('/book/<isbn>', methods=['GET', 'POST'])
def book(isbn):
    # if send to this route normally
    # query about book details from db
    book = Book.query.get(isbn)
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": api_key, "isbns": isbn})

    if res.status_code != 200:
        return render_template('index.html', errmsg='GoodReads Data not found')
    else :    
        gr_ratings = res.json()
        gr_ratings = gr_ratings['books'][0]

    if request.method == 'GET':
        
        if not book:
            return render_template('index.html', errmsg='No records for this book')
        # found on DB
        else:
            all_ratings = UserReview.query.filter_by(isbn=isbn)
            for i_user in all_ratings:
                if i_user.userid == session['user_name']:
                    return render_template('book.html', book=book, ratings=gr_ratings, user_submitted=True, all_ratings=all_ratings)

            return render_template('book.html', book=book, ratings=gr_ratings, all_ratings=all_ratings)
    else:
        #if review submitted
        try:
            rating_val = int(request.form.get('rating'))
        except ValueError:
            return render_template('book.html', book=book, ratings=gr_ratings, errmsg='Ratings was not provided')
            
        if not request.form.get('review'):
            return render_template('book.html', book=book, ratings=gr_ratings, errmsg='Reveiw was not provided')
        
        user_review = UserReview(session['user_name'], isbn, rating_val, request.form.get('review'))
        db.session.add(user_review)
        db.session.commit()
        return redirect('/book/' + isbn)

@app.route('/api/<string:isbn>')
def api(isbn):
    book = Book.query.get(isbn)
    if not book:
        return jsonify({"Error": "ISBN not found"}), 404
    else:
        #create dictionary for the book here 
        user_ratings = UserReview.query.filter_by(isbn = isbn)
        avg = count = 0
        for each_rating in user_ratings:
            avg += each_rating.rating
            count += 1
        if count != 0:
            avg = avg/count
        res = {'title': book.title, 'author': book.author, 'year': book.year, 'isbn': book.isbn, 'review_count': count, 'average_score': avg}
        return jsonify(res)
        
if __name__=='__main__':
    app.run(debug=True)
