from flask import render_template, url_for, flash, redirect
from app import app
# Unused -> from flask_table import Table, Col

try:
    from .forms import LoginForm
except:
    print("An error has occurred importing [Form] module.")
    print("")
try:
    from .services.telephony.contacts import CompanyContacts
    from .services.telephony.sms import sms_response, sms_check_in_data
    from .services.telephony.calls import call_response, call_check_in_data
except:
    print("An error has occurred importing [Telephony] module.")
    print("")


# - Variables
logged_in = False


# - Root Path
@app.route('/')
@app.route('/dashboard')
def index(logged_in=logged_in):
# def index(logged_in=True):
    username = ""

    if logged_in == False:
        return redirect(url_for('login'))
    else:
        return render_template('core_modules/dashboard/index.html',
                           module_name="Just-a-Dash Control Panel",
                           page_name="Dashboard",
                           icon="fa fa-dashboard",
                           logged_in=logged_in,
                           username=username)


# - Core Modules
@app.route('/account-settings')
def account_settings(logged_in=logged_in):
    if logged_in == False:
        return redirect(url_for('login'))
    else:
        return render_template('core_modules/account_settings/index.html',
                               icon="fa fa-dashboard",
                               module_abbreviation="Account Settings",
                               module_name="Account Settings",
                               page_name="Account Settings Home",
                               logged_in=logged_in)


@app.route('/app-settings')
def app_settings(logged_in=logged_in):
    if logged_in == False:
        return redirect(url_for('login'))
    else:
        return render_template('core_modules/app_settings/index.html',
                               icon="fa fa-dashboard",
                               module_abbreviation="App Settings",
                               module_name="App Settings",
                               page_name="App Settings Home",
                               logged_in=logged_in)


@app.route('/login', methods=['GET', 'POST'])
def login(logged_in=logged_in):
    form = LoginForm()
    
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me="%s"' %
              form.openid.data, str(form.remember_me.data))
        return redirect('/')

    return render_template('core_modules/login/index.html',
                           logged_in=logged_in,
                           login_form=form)


# @app.route('/register')
# def register(logged_in=False):
#     if logged_in == False:
#         return redirect(url_for('login'))
#     else:
#         return render_template('core_modules/register/index.html')


@app.route('/profile')
def profile(logged_in=logged_in):
    if logged_in == False:
        return redirect(url_for('login'))
    else:
        return render_template('core_modules/profile/index.html',
                               icon="fa fa-dashboard",
                               module_abbreviation="Profile",
                               module_name="Profile",
                               page_name="Profile Home",
                               logged_in=logged_in)


# - Modules
@app.route('/hr')
@app.route('/hrm')
def hrm(logged_in=logged_in):
    if logged_in == False:
        return redirect(url_for('login'))
    else:
        try:
            personnel = CompanyContacts.get_contacts()
        except:
            personnel = CompanyContacts.get_contacts()
            # personnel = {"-": {"timestamp": "-", "first_name": "-", "last_name": "-", "phone_number": "-"}}

        return render_template('modules/hrm/index.html',
                               icon="fa fa-users",
                               module_abbreviation="HRM",
                               module_name="Human Resource Management",
                               page_name="HRM Home",
                               form_title="Personnel",
                               logged_in=logged_in,
                               personnel_data=personnel)


@app.route('/crm')
def crm(logged_in=logged_in):
    if logged_in == False:
        return redirect(url_for('login'))
    else:
        try:
            customers = CompanyContacts.get_customer_contacts()
        except:
            customers = {"-": {"timestamp": "-", "first_name": "-", "last_name": "-", "phone_number": "-"}}

        return render_template('modules/crm/index.html',
                               icon="ion-person-stalker",
                               module_abbreviation="CRM",
                               module_name="Customer Relationship Management",
                               page_name="CRM Home",
                               form_title="Customer",
                               logged_in=logged_in,
                               customer_data=customers)


@app.route('/operations')
def operations(*args, logged_in=logged_in):
    if logged_in == False:
        return redirect(url_for('login'))
    else:
        try:
            check_in_type = args[0]
        except:
            check_in_type = None

        if check_in_type == "sms_check_in":
            check_in_entries = sms_check_in_data()
        elif check_in_type == "call_check_in":
            check_in_entries = call_check_in_data()
        elif check_in_type == None:
            check_in_entries = call_check_in_data()
        else:
            check_in_entries = {".": {"timestamp": ".", "first_name": ".", "last_name": ".", "phone_number": "."}}

        return render_template('modules/operations/index.html',
                               icon="fa fa-fort-awesome",
                               module_abbreviation="OMS",
                               module_name="Operations Management",
                               page_name="OMS Home",
                               logged_in=logged_in,
                               check_in_entries=check_in_entries)


@app.route('/checkin')
@app.route('/check-in')
@app.route('/callin')
@app.route('/call-in')
def call_check_in(logged_in=logged_in):
    if logged_in == False:
        return redirect(url_for('login'))
    else:
        return operations("call_check_in",
                           logged_in=logged_in,)


@app.route('/textin')
@app.route('/text-in')
@app.route('/text-checkin')
@app.route('/sms-checkin')
def sms_check_in(logged_in=logged_in):
    if logged_in == False:
        return redirect(url_for('login'))
    else:
        return operations("sms_check_in",
                           logged_in=logged_in,)



@app.route('/bms')
@app.route('/billing')
@app.route('/ams')
@app.route('/accounting')
def accounting(logged_in=logged_in):
    if logged_in == False:
        return redirect(url_for('login'))
    else:
        return render_template('modules/accounting/index.html',
                               icon="fa fa-bar-chart",
                               module_abbreviation="AMS",
                               module_name="Accounting Management",
                               page_name="AMS Home",
                               logged_in=logged_in,)


@app.route('/mms')
@app.route('/marketing')
def marketing(logged_in=True):
    if logged_in == False:
        return redirect(url_for('login'))
    else:
        return render_template('modules/marketing/index.html',
                               icon="fa fa-line-chart",
                               module_abbreviation="MMS",
                               module_name="Marketing Management",
                               page_name="MMS Home",
                               logged_in=logged_in,)


# - Services
@app.route('/sms')
@app.route('/sms_send')
@app.route('/sms_receive')
def sms():
    return sms_response()


@app.route('/call', methods=['GET', 'POST'])
@app.route('/calls', methods=['GET', 'POST'])
@app.route('/call_send', methods=['GET', 'POST'])
@app.route('/call_receive', methods=['GET', 'POST'])
def call():
    return call_response()


if __name__ == "__main__":
    print("yolo")
