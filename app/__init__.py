#!/usr/bin/env python
from flask import Flask
from flask_adminlte import AdminLTE
from flask_sqlalchemy import SQLAlchemy


# - Initialize App
print("##### Just-a-Dash ERP Dashboard #####")
app = Flask(__name__)


# - Initialize DB
app.config['SQL_ALCHEMY_URI'] = 'postgresql+psycopg2://postgres:Megaman40oz@localhost/justadash'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

def setup_db():
    temp_var = True  # Will refacror this.
    if temp_var:
        from app import db
        db.create_all()
    else:
        print("Error. Could not setup DB. Either an exception occurred, or the DB is already setup.")

setup_db()

# - Initialize UI Theme
from app import routes
AdminLTE(app)


# - Contingencies
# Run - Allows running of app directly from this file.
if __name__ == '__main__':
    app().run(debug=True)
