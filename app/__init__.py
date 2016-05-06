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
###     Init DB    ###
######################
db = SQLAlchemy(app)
from .models import App_Config, User, Result

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

######################
###  Blueprints   ###
######################


######################
###    Sessions    ###
######################
try:
    app.secret_key = App_Config.query.filter_by(key='Secret Key').first().value
except:
    print('Exception. Main __init__.py attempted to set Secret Key value based on DB value, but an error occurred.'
          'This is likely due to one of the following reasons: (1) You are running db_create.py, or (2) You are '
          'attempting to run the application for the first time, but have not populated the database by running '
          'db_create.py. If (2), run db_create.py. If (1), this error is expected, and perfectly alright.')
login_manager.login_view = 'login'

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
