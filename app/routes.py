try:
    # - Framework Imports
    from flask import render_template
    # Imports to be incorporated later.
    # from flask import url_for

    # - App Imports
    from app import app

    # - Services Imports
    # import twilio.twiml
    from .services.sms.sms import sms_response
    # from sms_io import sms_response
except:
    # - Framework Imports
    from flask import render_template
    # Imports to be incorporated later.
    # from flask import url_for

    # - App Imports
    from app import app

    # - Services Imports
    # import twilio.twiml
    from sms import sms_response
    # from sms_io import sms_response


# - Root Path
@app.route('/')
@app.route('/dashboard')
def index():
    module_name = "Dashboard"
    page_name = "Home"

    logged_in = False

    username = ""

    return render_template('core_modules/dashboard/index.html',
                           module_name=module_name,
                           page_name=page_name,
                           logged_in=logged_in,
                           username=username)

# - Core Modules
@app.route('/account-settings')
def account_settings():
    module_name = "Account Settings"
    page_name = "Home"
    return render_template('core_modules/account_settings/index.html',
                           module_name=module_name,
                           page_name=page_name)

@app.route('/app-settings')
def app_settings():
    module_name = "App Settings"
    page_name = "Home"
    return render_template('core_modules/app_settings/index.html',
                           module_name=module_name,
                           page_name=page_name)


@app.route('/login')
def login():
    return render_template('core_modules/login/index.html')


@app.route('/register')
def register():
    return render_template('core_modules/register/index.html')


@app.route('/profile')
def profile():
    module_name = "Profile"
    page_name = "Home"
    return render_template('core_modules/profile/index.html',
                           module_name=module_name,
                           page_name=page_name)


# - Modules
@app.route('/hrm')
def hrm():
    module_name = "HRM"
    page_name = "Home"
    return render_template('modules/hrm/index.html',
                           module_name=module_name,
                           page_name=page_name)


@app.route('/crm')
def crm():
    module_name = "CRM"
    page_name = "Home"
    return render_template('modules/crm/index.html',
                           module_name=module_name,
                           page_name=page_name)


@app.route('/operations')
def operations():
    module_name = "OMS"
    page_name = "Home"
    return render_template('modules/operations/index.html',
                           module_name=module_name,
                           page_name=page_name)


@app.route('/accounting')
def accounting():
    module_name = "AMS"
    page_name = "Home"
    return render_template('modules/accounting/index.html',
                           module_name=module_name,
                           page_name=page_name)


# - Services
@app.route('/sms_receive')
def sms_receive():
    return sms_response()

@app.route('/sms')
@app.route('/sms_send')
def sms_send():
    return ""
