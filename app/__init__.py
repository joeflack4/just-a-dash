#!/usr/bin/env python
######################
###     Imports    ###
######################
import os
from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask_adminlte import AdminLTE
from .config import Config

# 1. Tutorial 1 Import
try:
    from flask.ext.sqlalchemy import SQLAlchemy
except:
    from flask_sqlalchemy import SQLAlchemy


######################
### Initialize App ###
######################
app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

######################
###   Init Config  ###
######################
try:
    app.config.from_object(os.environ['APP_SETTINGS'])
except KeyError:
    # If environment variable 'APP_SETTINGS' isn't defined by administrator, exception defaults to development settings.
    app.config.from_object(config.DevelopmentConfig)
except:
    # Backup exception.
    app.config.from_object(config.DevelopmentConfig)

# - Initialize DB
# 1. Tutorial 1
# app.config['SQL_ALCHEMY_URI'] = 'postgresql+psycopg2://joeflack4:pizzaLatte186*@localhost/justadash'
db = SQLAlchemy(app)
from .models import Result


# # # My added magic # # #
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)
#
#     def __init__(self, username, email):
#         self.username = username
#         self.email = email
#
#     def __repr__(self):
#         return '<User %r>' % self.username
#
# def setup_db():
#     temp_var = True  # Will refactor this.
#     if temp_var:
#         from app import db
#         db.create_all()
#     else:
#         print("Error. Could not setup DB. Either an exception occurred, or the DB is already setup.")
#
# setup_db()
# # # My added magic # # #


# 2. Tutorial 2
# DATABASE_URL = "postgresql://localhost/wordcount_dev"
# os.environ["DATABASE_URL"] = 'postgresql+psycopg2://joeflack4:pizzaLatte186*@localhost/justadash'
# app.config.from_object(config.DevelopmentConfig)

#
# try:
#     app.config.from_object(os.environ['DATABASE_URL'])
#     print(os.environ['DATABASE_URL'])
# except KeyError as e:
#     os.environ["DATABASE_URL"] = 'postgresql+psycopg2://joeflack4:pizzaLatte186*@localhost/justadash'
#     app.config.from_object(config.DevelopmentConfig)
#     print(os.environ['DATABASE_URL'])
# except:
#     os.environ["DATABASE_URL"] = 'postgresql+psycopg2://joeflack4:pizzaLatte186*@localhost/justadash'
#     app.config.from_object(config.DevelopmentConfig)
#     print(os.environ['DATABASE_URL'])
#     pass
#


######################
###  Blueprints   ###
######################


######################
###    Sessions    ###
######################
from .models import User
# - may need to change thsi
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

######################
### Initialize UI  ###
######################
from app import routes
AdminLTE(app)


# - Contingencies
if __name__ == '__main__':
    # Run: Allows running of app directly from this file.
    app().run(debug=True)
