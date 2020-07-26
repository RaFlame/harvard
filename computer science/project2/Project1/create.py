import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


def Create():
    print('Please Wait...')
    db.create_all()
    print('Tables Created!')

if __name__ == "__main__":
    with app.app_context():
       Create()