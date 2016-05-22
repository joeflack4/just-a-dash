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
# from flask.ext.login import LoginManager, current_user
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
# from flask.ext.restless import APIManager, ProcessingException
from flask_adminlte import AdminLTE
from .config import Config
from .api import ApiAuth


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
from .models import AppConfig, User, Result, Customers, Personnel
from .models import Modules, Roles, Permissions, Messages, AppNotifications, Contacts, CrmConfig, Agencies, OmsConfig,\
    MmsConfig, HrmConfig

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
    app.secret_key = AppConfig.query.filter_by(key='Secret Key').first().value
except:
    exceptions[1] = True

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

######################
###      API       ###
######################
api_manager = APIManager(app, flask_sqlalchemy_db=db)

# - API's which connect to current user data. (yet unimplemented)
# messages_api_blueprint = api_manager.create_api(Messages, collection_name='messages', methods=['GET', 'POST', 'DELETE',
#                                                 'PUT'], preprocessors=dict(GET_SINGLE=[API_Auth.logged_in],
#                                                 GET_MANY=[API_Auth.logged_in]))

# - API's requiring basic admin status.
contacts_api_blueprint = api_manager.create_api(Contacts, collection_name='contacts', methods=['GET', 'POST', 'DELETE',
                                                'PUT'],preprocessors=dict(GET_SINGLE = [ApiAuth.basic_admin],
                                                GET_MANY = [ApiAuth.basic_admin]))

# - API's requiring basic CRM admin status.
customers_api_blueprint = api_manager.create_api(Customers, collection_name='customers',
                                                 methods=['GET', 'POST', 'DELETE', 'PUT'],
                                                 preprocessors=dict(GET_SINGLE=[ApiAuth.basic_crm_admin],
                                                 GET_MANY=[ApiAuth.basic_crm_admin]))
agencies_api_blueprint = api_manager.create_api(Agencies, collection_name='agencies',
                                                methods=['GET', 'POST', 'DELETE', 'PUT'],
                                                preprocessors=dict(GET_SINGLE=[ApiAuth.basic_crm_admin],
                                                                   GET_MANY=[ApiAuth.basic_crm_admin]))

# - API's requiring basic HRM admin status.
personnel_api_blueprint = api_manager.create_api(Personnel, collection_name='personnel',
                                                 methods=['GET', 'POST', 'DELETE', 'PUT'],
                                                 preprocessors=dict(GET_SINGLE=[ApiAuth.basic_hrm_admin], GET_MANY=[ApiAuth.basic_hrm_admin]))

# - API's requiring basic MMS admin status.
result_api_blueprint = api_manager.create_api(Result, collection_name='keyword-analysis-results',
                                              methods=['GET', 'POST', 'DELETE', 'PUT'],
                                              preprocessors=dict(GET_SINGLE=[ApiAuth.basic_mms_admin], GET_MANY=[ApiAuth.basic_mms_admin]))

# - API's requiring super admin status.
app_notifications_api_blueprint = api_manager.create_api(AppNotifications, collection_name='app-notifications',
                                                         methods=['GET', 'POST', 'DELETE', 'PUT'],
                                                         preprocessors=dict(GET_SINGLE=[ApiAuth.super_admin],
                                                         GET_MANY=[ApiAuth.super_admin]))
roles_api_blueprint = api_manager.create_api(Roles, collection_name='user-roles', methods=['GET', 'POST', 'DELETE',
                                             'PUT'], preprocessors=dict(GET_SINGLE=[ApiAuth.super_admin],
                                             GET_MANY=[ApiAuth.super_admin]))
permissions_api_blueprint = api_manager.create_api(Permissions, collection_name='user-permissions', methods=['GET',
                                                   'POST', 'DELETE', 'PUT'], preprocessors=dict(
                                                    GET_SINGLE=[ApiAuth.super_admin], GET_MANY=[ApiAuth.super_admin]))
modules_api_blueprint = api_manager.create_api(Modules, collection_name='modules', methods=['GET', 'POST', 'DELETE',
                                               'PUT'], preprocessors=dict(GET_SINGLE=[ApiAuth.super_admin],
                                                GET_MANY=[ApiAuth.super_admin]))
crm_config_api_blueprint = api_manager.create_api(CrmConfig, collection_name='crm-config', methods=['GET', 'POST',
                                                  'DELETE', 'PUT'], preprocessors=dict(
                                                  GET_SINGLE=[ApiAuth.super_admin], GET_MANY=[ApiAuth.super_admin]))
hrm_config_api_blueprint = api_manager.create_api(HrmConfig, collection_name='hrm-config', methods=['GET', 'POST',
                                                  'DELETE', 'PUT'], preprocessors=dict(
                                                  GET_SINGLE=[ApiAuth.super_admin], GET_MANY=[ApiAuth.super_admin]))
oms_config_api_blueprint = api_manager.create_api(OmsConfig, collection_name='oms-config', methods=['GET', 'POST',
                                                  'DELETE', 'PUT'], preprocessors=dict(
                                                  GET_SINGLE=[ApiAuth.super_admin], GET_MANY=[ApiAuth.super_admin]))
mms_config_api_blueprint = api_manager.create_api(MmsConfig, collection_name='mms-config', methods=['GET', 'POST',
                                                  'DELETE', 'PUT'], preprocessors=dict(
                                                  GET_SINGLE=[ApiAuth.super_admin], GET_MANY=[ApiAuth.super_admin]))
app_config_api_blueprint = api_manager.create_api(AppConfig, collection_name='app-config', methods=['GET', 'POST',
                                                  'DELETE', 'PUT'], preprocessors=dict(GET_SINGLE=[ApiAuth.super_admin],
                                                  GET_MANY=[ApiAuth.super_admin]))

# - API's requiring super admin status.
# -- Note: This API is just a redundant copy of the 'app-config' API under a different name and permission setting. It
# exists solely to test the 'master admin' permissions requirement.
master_config_api_blueprint = api_manager.create_api(AppConfig, collection_name='master-config', methods=['GET', 'POST',
                                                     'DELETE', 'PUT'], preprocessors=dict(
                                                      GET_SINGLE=[ApiAuth.master_admin], GET_MANY=[ApiAuth.master_admin]))

######################
### Initialize UI  ###
######################
try:
    from app import routes
    AdminLTE(app)
except:
    exceptions[1] = True

if exceptions != {}:
    if exceptions[1]:
        script_being_run = sys.argv[0]
        if script_being_run != 'manage.py':
            print('')
            print('Exception #1. Main __init__.py attempted to set Secret Key value based on DB value, but an error '
                  'occurred. This is likely due to one of the following reasons: (1) You are running db_create.py, or '
                  '(2) You are attempting to run the application for the first time, but have not populated the '
                  'database by running db_create.py. If (2), run db_create.py. If (1), this error is expected, and '
                  'perfectly alright.')
            print('')

# - Contingencies
if __name__ == '__main__':
    # Run: Allows running of app directly from this file.
    app().run(debug=True)
