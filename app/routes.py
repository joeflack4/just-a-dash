from flask import render_template
from app import app
# # Unused -> from flask import url_for
# # Unused -> from flask_table import Table, Col

try:
    from .services.telephony.contacts import CompanyContacts
    from .services.telephony.sms import sms_response, check_in_data
    from .services.telephony.calls import call_response
except:
    from .services.telephony.sms import sms_response, check_in_data, CompanyContacts
    from .services.telephony.calls import call_response

# - Root Path
@app.route('/')
@app.route('/dashboard')
def index():
    logged_in = False
    username = ""

    return render_template('core_modules/dashboard/index.html',
                           module_name="Just-a-Dash Control Panel",
                           page_name="Dashboard",
                           icon="fa fa-dashboard",
                           logged_in=logged_in,
                           username=username)

# - Core Modules
@app.route('/account-settings')
def account_settings():
    return render_template('core_modules/account_settings/index.html',
                           icon="fa fa-dashboard",
                           module_abbreviation="Account Settings",
                           module_name="Account Settings",
                           page_name="Account Settings Home")

@app.route('/app-settings')
def app_settings():
    return render_template('core_modules/app_settings/index.html',
                           icon="fa fa-dashboard",
                           module_abbreviation="App Settings",
                           module_name="App Settings",
                           page_name="App Settings Home")


@app.route('/login')
def login():
    return render_template('core_modules/login/index.html')


@app.route('/register')
def register():
    return render_template('core_modules/register/index.html')


@app.route('/profile')
def profile():
    return render_template('core_modules/profile/index.html',
                           icon="fa fa-dashboard",
                           module_abbreviation="Profile",
                           module_name="Profile",
                           page_name="Profile Home")


# - Modules
@app.route('/hrm')
def hrm():
    try:
        personnel = CompanyContacts.get_contacts()
    except:
        personnel = {"-": {"timestamp": "-", "first_name": "-", "last_name": "-", "phone_number": "-"}}

    return render_template('modules/hrm/index.html',
                           icon="fa fa-users",
                           module_abbreviation="HRM",
                           module_name="Human Resource Management",
                           page_name="HRM Home",
                           form_title="Personnel",
                           personnel_data=personnel)


@app.route('/crm')
def crm():
    try:
        # customers = CompanyContacts.get_customer_contacts()
        customers = {"-": {"timestamp": "-", "first_name": "-", "last_name": "-", "phone_number": "-"}}
    except:
        customers = {"-": {"timestamp": "-", "first_name": "-", "last_name": "-", "phone_number": "-"}}

    return render_template('modules/crm/index.html',
                           icon="ion-person-stalker",
                           module_abbreviation="CRM",
                           module_name="Customer Relationship Management",
                           page_name="CRM Home",
                           form_title="Customer",
                           customer_data=customers)


@app.route('/operations')
@app.route('/checkin')
@app.route('/check-in')
def operations():
    try:
        check_in_entries = check_in_data()
    except:
        check_in_entries = {"-": {"timestamp": "-", "first_name": "-", "last_name": "-", "phone_number": "-"}}

    return render_template('modules/operations/index.html',
                           icon="fa fa-fort-awesome",
                           module_abbreviation="OMS",
                           module_name="Operations Management",
                           page_name="OMS Home",
                           check_in_entries=check_in_entries)


@app.route('/accounting')
def accounting():
    return render_template('modules/accounting/index.html',
                           icon="fa fa-bar-chart",
                           module_abbreviation="AMS",
                           module_name="Accounting Management",
                           page_name="AMS Home")


# - Services
@app.route('/sms')
@app.route('/sms_send')
@app.route('/sms_receive')
def sms():
    return sms_response()


@app.route('/call')
@app.route('/calls')
@app.route('/call_send')
@app.route('/call_receive')
def call():
    return call_response()
