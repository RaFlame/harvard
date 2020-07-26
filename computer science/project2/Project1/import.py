import csv, os

from flask import Flask
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

def Import():
    csv_file = csv.reader(open('books.csv'))
    count = 0
    for isbn, title, author, year in csv_file:
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
        count +=1

    print('Please Wait...')
    db.session.commit()
    print(f'Successfully added {count} books!')

if __name__ == "__main__":
    with app.app_context():
        Import()