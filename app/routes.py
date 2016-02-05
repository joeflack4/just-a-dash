# - Framework Imports
from flask import render_template
# Imports to be incorporated later.
# from flask import url_for

# - App Imports
from app import app

# - Services Imports
import twilio.twiml


# - Root Path
@app.route('/')
@app.route('/dashboard')
def index():
    username = ""
    return render_template('core_modules/dashboard/index.html',
                           username=username)

#@app.route('/dashboard')
#def dashboard():
#    page_header = "Welcome to the Pythonic Dashboard."
#    return render_template('core_modules/dashboard/index.html',
#                           page_header=page_header)

# - Core Modules
@app.route('/account-settings')
def account_settings():
    return render_template('core_modules/account_settings/index.html')


@app.route('/app-settings')
def app_settings():
    return render_template('core_modules/app_settings/index.html')


@app.route('/login')
def login():
    return render_template('core_modules/login/index.html')


@app.route('/register')
def register():
    return render_template('core_modules/register/index.html')


@app.route('/profile')
def profile():
    return render_template('core_modules/profile/index.html')


# - Modules							  
@app.route('/hrm')
def hrm():
    return render_template('modules/hrm/index.html')


@app.route('/crm')
def crm():
    return render_template('modules/crm/index.html')


@app.route('/operations')
def operations():
    return render_template('modules/operations/index.html')


@app.route('/accounting')
def accounting():
    return render_template('modules/accounting/index.html')


# - Services
@app.route('/sms_receive')
def sms_receive():
    resp = twilio.twiml.Response()
    resp.message("Hello there.")
    return str(resp)


@app.route('/sms_respond')
def sms_respond():
    return ""


@app.route('/sms_send')
def sms_send():
    return ""
