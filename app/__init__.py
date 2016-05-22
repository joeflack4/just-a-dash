#!/usr/bin/env python
######################
###     Imports    ###
######################
# import os
import os
import sys
from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
# - careful
# import flask
# import flask.ext.sqlalchemy
# import flask.ext.restless


from flask_adminlte import AdminLTE
from .config import Config
# - careful
# try:
#     from flask.ext.sqlalchemy import SQLAlchemy
# except:
#     from flask_sqlalchemy import SQLAlchemy


######################
### Initialize App ###
######################
exceptions = {}
app = Flask(__name__)
# app.config.from_object('config')
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

######################
###     Init DB    ###
######################
db = SQLAlchemy(app)
# - careful
# db = flask.ext.sqlalchemy.SQLAlchemy(app)
from .models import App_Config, User, Result, Customers, Personnel
from .models import Modules, Roles, Permissions, Messages, AppNotifications, Contacts, CRM_Config, Agencies, OMS_Config, MMS_Config

######################
###      API       ###
######################
api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Customers, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(App_Config, methods=['GET', 'POST', 'DELETE', 'PUT']) # OK
api_manager.create_api(Result, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(Personnel, methods=['GET', 'POST', 'DELETE', 'PUT'])

api_manager.create_api(Modules, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(Roles, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(Permissions, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(Messages, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(AppNotifications, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(Contacts, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(CRM_Config, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(Agencies, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(OMS_Config, methods=['GET', 'POST', 'DELETE', 'PUT'])
api_manager.create_api(MMS_Config, methods=['GET', 'POST', 'DELETE', 'PUT'])

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
    exceptions[1] = True

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

######################
### Initialize UI  ###
######################
try:
    from app import routes
    AdminLTE(app)
except:
    exceptions[1] = True

if exceptions != {}:
    if exceptions[1] == True:
        script_being_run = sys.argv[0]
        if script_being_run != 'manage.py':
            print('')
            print('Exception #1. Main __init__.py attempted to set Secret Key value based on DB value, but an error occurred.'
                  'This is likely due to one of the following reasons: (1) You are running db_create.py, or (2) You are '
                  'attempting to run the application for the first time, but have not populated the database by running '
                  'db_create.py. If (2), run db_create.py. If (1), this error is expected, and perfectly alright.')
            print('')

# - Contingencies
if __name__ == '__main__':
    # Run: Allows running of app directly from this file.
    app().run(debug=True)
