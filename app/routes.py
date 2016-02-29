try:
    # - Framework Imports
    from flask import render_template
    # - Flask Imports to be incorporated later.
    # from flask import url_for
    # from flask_table import Table, Col

    # - App Imports
    from app import app

    # - Services Imports
    # import twilio.twiml
    # from sms_io import sms_response
    from .services.sms.sms import sms_response, check_in_data
except:
    from flask import render_template
    from app import app
    from sms import sms_response, check_in_data


# - Root Path
@app.route('/')
@app.route('/dashboard')
def index():
    module_name = "Admin Control Panel"
    page_name = "Dashboard"
    icon = "fa fa-dashboard"

    logged_in = False
    username = ""

    return render_template('core_modules/dashboard/index.html',
                           module_name=module_name,
                           page_name=page_name,
                           icon=icon,
                           logged_in=logged_in,
                           username=username)

# - Core Modules
@app.route('/account-settings')
def account_settings():
    module_abbreviation = "Account Settings"
    module_name = "Account Settings"
    page_name = "Account Settings Home"
    icon = "fa fa-dashboard"
    return render_template('core_modules/account_settings/index.html',
                           icon=icon,
                           module_abbreviation=module_abbreviation,
                           module_name=module_name,
                           page_name=page_name)

@app.route('/app-settings')
def app_settings():
    module_abbreviation = "App Settings"
    module_name = "App Settings"
    page_name = "App Settings Home"
    icon = "fa fa-dashboard"
    return render_template('core_modules/app_settings/index.html',
                           icon=icon,
                           module_abbreviation=module_abbreviation,
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
    module_abbreviation = "Profile"
    module_name = "Profile"
    page_name = "Profile Home"
    icon = "fa fa-dashboard"
    return render_template('core_modules/profile/index.html',
                           icon=icon,
                           module_abbreviation=module_abbreviation,
                           module_name=module_name,
                           page_name=page_name)


# - Modules
@app.route('/hrm')
def hrm():
    module_abbreviation = "HRM"
    module_name = "Human Resource Management"
    page_name = "HRM Home"
    icon = "fa fa-users"
    return render_template('modules/hrm/index.html',
                           icon=icon,
                           module_abbreviation=module_abbreviation,
                           module_name=module_name,
                           page_name=page_name)


@app.route('/crm')
def crm():
    module_abbreviation = "CRM"
    module_name = "Customer Relationship Management"
    page_name = "CRM Home"
    icon = "ion-ios-people"
    return render_template('modules/crm/index.html',
                           icon=icon,
                           module_abbreviation=module_abbreviation,
                           module_name=module_name,
                           page_name=page_name)


@app.route('/operations')
def operations():
    module_abbreviation = "OMS"
    module_name = "Operations Management"
    page_name = "OMS Home"
    icon = "fa fa-fort-awesome"

    try:
        check_in_entries = check_in_data()
    except:
        check_in_entries = {"-": {"timestamp": "-", "first_name": "-", "last_name": "-"}}

    return render_template('modules/operations/index.html',
                           icon=icon,
                           module_abbreviation=module_abbreviation,
                           module_name=module_name,
                           page_name=page_name,
                           check_in_entries=check_in_entries)


@app.route('/accounting')
def accounting():
    module_abbreviation = "AMS"
    module_name = "Accounting Management"
    page_name = "AMS Home"
    icon = "fa fa-dashboard"
    return render_template('modules/accounting/index.html',
                           icon=icon,
                           module_abbreviation=module_abbreviation,
                           module_name=module_name,
                           page_name=page_name)


# - Services
@app.route('/sms')
@app.route('/sms_receive')
@app.route('/sms_send')
def sms():
    return sms_response()
