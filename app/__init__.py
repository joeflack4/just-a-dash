#!/usr/bin/env python
import os
from .config import Config, DevelopmentConfig

from flask import Flask
from flask_adminlte import AdminLTE
from flask_sqlalchemy import SQLAlchemy


# - Initialize App
app = Flask(__name__)

# Set app settings to detect and react to the type of environment being run.
try:
    app.config.from_object(os.environ['APP_SETTINGS'])
    print(os.environ['APP_SETTINGS'])
except KeyError as e:
    # print("Exception: ", e, ": APP_SETTINGS not set. This may be your local development environment, or APP_SETTINGS has otherwise not been set on your test/staging/deployment environments.")
    # print("Exception has been handled by automatic runtime setting of APP_SETTINGS value.")
    os.environ["APP_SETTINGS"] = str(config.DevelopmentConfig)
    # app.config.from_object(os.environ['APP_SETTINGS'])
    app.config.from_object(config.DevelopmentConfig)
    print(os.environ['APP_SETTINGS'])
except:
    # print("Error: Unexpected exception occured when trying to apply APP_SETTINGS. This may be your local development environment, or APP_SETTINGS has otherwise not been set on your test/staging/deployment environments.")
    # print("Exception has been handled by automatic runtime setting of APP_SETTINGS value.")
    os.environ["APP_SETTINGS"] = str(config.DevelopmentConfig)
    app.config.from_object(config.DevelopmentConfig)
    print(os.environ['APP_SETTINGS'])
    pass


# - Initialize DB
app.config['SQL_ALCHEMY_URI'] = 'postgresql+psycopg2://joeflack4:pizzaLatte186*@localhost/justadash'
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
    temp_var = True  # Will refactor this.
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
if __name__ == '__main__':
    # Run: Allows running of app directly from this file.
    app().run(debug=True)
