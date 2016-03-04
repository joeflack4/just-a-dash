# This code is not currently being used by the app. Will later use this instead of including the model in app initialization.

# from flask_sqlalchemy import SQLAlchemy
# from app import app
# from app import db
db = ""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
