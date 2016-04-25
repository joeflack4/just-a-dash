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
db = SQLAlchemy(app)
from .models import Result

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
