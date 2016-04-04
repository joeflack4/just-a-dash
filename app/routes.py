from flask import render_template, url_for, flash, redirect, request
from flask.ext.login import login_required, login_user, logout_user, current_user
from app import app, db, bcrypt

# from wtforms import SelectField
# from collections import namedtuple

# Unused -> from flask_table import Table, Col
# from functools import wraps

# Imports to be ported to eventual Marketing blueprint module.
import requests
from collections import Counter
from bs4 import BeautifulSoup
import operator
import re
import nltk
# more
from .stop_words import stops

try:
    from .models import User, Messages, Result, AppNotifications
except:
    print("An error has occurred importing [Models].")
    print("")
try:
    from .forms import LoginForm, RegisterForm, UserAddForm, UserUpdateForm, CustomerAddForm, CustomerUpdateForm, PersonnelAddForm, PersonnelUpdateForm
except:
    print("An error has occurred importing [Forms].")
    print("")
try:
    from .modals import user_add_modal, user_update_modal, customer_add_modal, customer_update_modal, personnel_add_modal, personnel_update_modal
except:
    print("An error has occurred importing [Modals].")
    print("")
try:
    from .services.telephony.contacts import CompanyContacts
    from .services.telephony.sms import sms_response, sms_check_in_data
    from .services.telephony.calls import call_response, call_check_in_data
except:
    print("An error has occurred importing [Telephony] module.")
    print("")


##############
# - Variables


##############
# - Decorators
# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args, **kwargs)
#         else:
#             flash('Please log in before proceeding.', 'warning')
#             return redirect(url_for('login'))
#     return wrap


##############
# - Root Path
@app.route('/')
def root_path():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    else:
        return redirect(url_for('welcome'))


@app.route('/welcome')
def welcome():
    logged_in = current_user.is_authenticated()
    user = current_user
    login_form = LoginForm(request.form)
    register_form = RegisterForm()
    return render_template('core_modules/welcome/index.html',
                           module_name="Just-a-Dash Control Panel",
                           page_name="Welcome",
                           icon="fa fa-star-o",
                           module_abbreviation="Home",
                           messages=db.session.query(Messages),
                           app_notifications=db.session.query(AppNotifications),
                           login_form=login_form,
                           register_form=register_form,
                           user=user,
                           logged_in=logged_in)


@app.route('/index')
@app.route('/dashboard')
@app.route('/home')
@login_required
def index():
    logged_in = current_user.is_authenticated()
    user = current_user
    login_form = LoginForm(request.form)
    return render_template('core_modules/dashboard/index.html',
                           module_name="Just-a-Dash Control Panel",
                           page_name="Dashboard",
                           icon="fa fa-dashboard",
                           module_abbreviation="Home",
                           messages=db.session.query(Messages),
                           app_notifications=db.session.query(AppNotifications),
                           login_form=login_form,
                           user=user,
                           logged_in=logged_in)


################
# - Core Modules
@app.route('/account-settings')
@login_required
def account_settings():
    logged_in = current_user.is_authenticated()
    user = current_user
    login_form = LoginForm(request.form)
    return render_template('core_modules/account_settings/index.html',
                           icon="fa fa-dashboard",
                           module_abbreviation="Account Settings",
                           module_name="Account Settings",
                           page_name="Account Settings Home",
                           messages=db.session.query(Messages),
                           app_notifications=db.session.query(AppNotifications),
                           login_form=login_form,
                           user=user,
                           logged_in=logged_in)


@app.route('/app-settings')
@login_required
def app_settings():
    logged_in = current_user.is_authenticated()
    user = current_user
    login_form = LoginForm(request.form)
    return render_template('core_modules/app_settings/index.html',
                           icon="fa fa-dashboard",
                           module_abbreviation="App Settings",
                           module_name="App Settings",
                           page_name="App Settings Home",
                           messages=db.session.query(Messages),
                           app_notifications=db.session.query(AppNotifications),
                           login_form=login_form,
                           user=user,
                           logged_in=logged_in)


@app.route('/user-management', methods=['GET', 'POST'])
@login_required
def user_management():
    logged_in = current_user.is_authenticated()
    user = current_user
    login_form = LoginForm(request.form)
    modals = {'UserAddModal': user_add_modal, 'UserUpdateModal': user_update_modal}

    # To do: Need to fix this so that my forms are able to create fields dynamically based on database values.
    # The code below doesn't seem to break app, but does not seem to have an effect.
    add_form = UserAddForm(request.form)
    update_form = UserUpdateForm(request.form)
    # db_populate_object = namedtuple('literal', 'name age')(**{'name': 'John Smith', 'age': 23})
    # add_form.append_field("test", SelectField('test'))(obj=db_populate_object)
    forms = {'User-Add-Form': add_form,
             'User-Update-Form': update_form}

    return render_template('core_modules/app_settings/user_management.html',
                           icon="fa fa-dashboard",
                           module_abbreviation="App Settings",
                           module_name="App Settings",
                           page_name="User Management",
                           messages=db.session.query(Messages),
                           app_notifications=db.session.query(AppNotifications),
                           login_form=login_form,
                           user=user,
                           logged_in=logged_in,
                           modals=modals,
                           forms=forms)


@app.route('/logout')
def logout():
    logged_in = current_user.is_authenticated()
    logout_user()
    flash(u'Logged out. Thank you, come again!', 'success')
    return redirect(url_for('welcome'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    logged_in = current_user.is_authenticated()
    user = current_user
    errors = []
    login_form = LoginForm(request.form)
    register_form = RegisterForm()

    if request.method == 'POST':
        if login_form.validate_on_submit():
            user = User.query.filter_by(username=request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                login_user(user)
                flash(u'Logged in. Welcome back!', 'success')
                return redirect(url_for('index'))
        else:
            errors.append('Invalid credentials. Please try again.')
            user = User.query.filter_by(username=request.form['username']).first()
            for error in errors:
                flash(error, 'danger')
    return render_template('core_modules/login/index.html',
                           icon="fa fa-dashboard",
                           module_abbreviation="Home",
                           module_name="Just-a-Dash Control Panel",
                           page_name="Login",
                           messages=db.session.query(Messages),
                           app_notifications=db.session.query(AppNotifications),
                           login_form=login_form,
                           register_form=register_form,
                           user=user,
                           logged_in=logged_in)


@app.route('/register', methods=['GET', 'POST'])
def register():
    logged_in = current_user.is_authenticated()
    user = current_user
    login_form = LoginForm(request.form)
    register_form = RegisterForm()
    if request.method == 'POST':
        if register_form.validate_on_submit():
            new_user = User(
                username=register_form.username.data,
                email=register_form.email.data,
                password=register_form.password.data)
            db.session.add(new_user)
            for item in db.session:
                item.password = item.password.decode("utf-8")
            db.session.commit()
            login_user(new_user)
            flash(u'Registration complete! You have been logged in.', 'success')
            return redirect(url_for('index'))
        else:
            flash(u'Registration failed. Please try again, or contact the site administrator. Ensure that: (1) Username is between 3-25 characters, (2) E-mail is between 6-40 characters, (3) Password is beteen 6-25 characters, (4) Password and confirm password are matching.', 'warning')

    return render_template('core_modules/register/index.html',
                           icon="fa fa-pencil-square-o",
                           module_abbreviation="Registration",
                           module_name="Registration",
                           page_name="New Submission",
                           messages=db.session.query(Messages),
                           app_notifications=db.session.query(AppNotifications),
                           login_form=login_form,
                           register_form=register_form,
                           user=user,
                           logged_in=logged_in)


@app.route('/profile')
@login_required
def profile():
    logged_in = current_user.is_authenticated()
    user = current_user
    login_form = LoginForm(request.form)
    return render_template('core_modules/profile/index.html',
                           icon="fa fa-dashboard",
                           module_abbreviation="Profile",
                           module_name="Profile",
                           page_name="Profile Home",
                           messages=db.session.query(Messages),
                           app_notifications=db.session.query(AppNotifications),
                           login_form=login_form,
                           user=user,
                           logged_in=logged_in)


############
# - Modules
@app.route('/hr', methods=['GET', 'POST'])
@app.route('/hrm', methods=['GET', 'POST'])
@login_required
def hrm():
    logged_in = current_user.is_authenticated()
    user = current_user
    login_form = LoginForm(request.form)
    modals = {'PersonnelAddModal': personnel_add_modal, 'PersonnelUpdateModal': personnel_update_modal}
    forms = {'Personnel-Add-Form': PersonnelAddForm(request.form),
             'Personnel-Update-Form': PersonnelUpdateForm(request.form)}

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
                                personnel_data=personnel,
                                messages=db.session.query(Messages),
                                app_notifications=db.session.query(AppNotifications),
                                login_form=login_form,
                                user=user,
                                logged_in=logged_in,
                                modals=modals,
                                forms=forms)


@app.route('/crm', methods=['GET', 'POST'])
@login_required
def crm():
    logged_in = current_user.is_authenticated()
    user = current_user
    login_form = LoginForm(request.form)
    modals = {'CustomerAddModal': customer_add_modal, 'CustomerUpdateModal': customer_update_modal}
    forms = {'Customer-Add-Form': CustomerAddForm(request.form),
             'Customer-Update-Form': CustomerUpdateForm(request.form)}

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
                           customer_data=customers,
                           messages=db.session.query(Messages),
                           app_notifications=db.session.query(AppNotifications),
                           login_form=login_form,
                           user=user,
                           logged_in=logged_in,
                           modals=modals,
                           forms=forms)


@app.route('/operations')
@login_required
def operations(*args):
    logged_in = current_user.is_authenticated()
    user = current_user
    login_form = LoginForm(request.form)
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
                           check_in_entries=check_in_entries,
                           messages=db.session.query(Messages),
                           app_notifications=db.session.query(AppNotifications),
                           login_form=login_form,
                           user=user,
                           logged_in=logged_in)


@app.route('/checkin')
@app.route('/check-in')
@app.route('/callin')
@app.route('/call-in')
@login_required
def call_check_in():
    return operations("call_check_in")


@app.route('/textin')
@app.route('/text-in')
@app.route('/text-checkin')
@app.route('/sms-checkin')
@login_required
def sms_check_in():
    return operations("sms_check_in")


@app.route('/bms')
@app.route('/billing')
@app.route('/ams')
@app.route('/accounting')
@login_required
def accounting():
    logged_in = current_user.is_authenticated()
    user = current_user
    login_form = LoginForm(request.form)
    return render_template('modules/accounting/index.html',
                           icon="fa fa-bar-chart",
                           module_abbreviation="AMS",
                           module_name="Accounting Management",
                           page_name="AMS Home",
                           messages=db.session.query(Messages),
                           app_notifications=db.session.query(AppNotifications),
                           login_form=login_form,
                           user=user,
                           logged_in=logged_in)


@app.route('/mms', methods=['GET', 'POST'])
@app.route('/marketing', methods=['GET', 'POST'])
@login_required
def marketing():
    logged_in = current_user.is_authenticated()
    user = current_user
    errors = []
    results = {}
    login_form = LoginForm(request.form)
    if request.method == "POST":
        try:
            url = request.form['url']
            # See if URL submitted contains 'http://' prepended.
            if url.find("http://") == 0:
                # r = requests.get(url).text.encode("utf-8")
                # r = requests.get(url).text
                r = requests.get(url)
                # print(r)
            else:
                url = "http://" + url
                r = requests.get(url)
        except:
            errors.append('Unable to get URL. Please make sure it\'s valid and try again.')
            return render_template('modules/marketing/index.html',
                                   icon="fa fa-line-chart",
                                   module_abbreviation="MMS",
                                   module_name="Marketing Management",
                                   page_name="MMS Home",
                                   errors=errors,
                                   messages=db.session.query(Messages),
                                   app_notifications=db.session.query(AppNotifications),
                                   login_form=login_form,
                                   user=user,
                                   logged_in=logged_in)

        if r:
            # text processing
            raw = BeautifulSoup(r.text).get_text()
            nltk.data.path.append('./nltk_data/')  # set the path
            tokens = nltk.word_tokenize(raw)
            text = nltk.Text(tokens)

            # remove punctuation, count raw words
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)

            # stop words
            no_stop_words = [w for w in raw_words if w.lower() not in stops]
            no_stop_words_count = Counter(no_stop_words)

            # save the results
            results = sorted(
                no_stop_words_count.items(),
                key=operator.itemgetter(1),
                reverse=True
            )[0:10]

            try:
                result = Result(
                    url=url,
                    result_all=raw_word_count,
                    result_no_stop_words=no_stop_words_count)
                db.session.add(result)
                db.session.commit()
            except:
                errors.append("Unable to add item to database.")

    return render_template('modules/marketing/index.html',
                           icon="fa fa-line-chart",
                           module_abbreviation="MMS",
                           module_name="Marketing Management",
                           page_name="MMS Home",
                           errors=errors,
                           results=results,
                           messages=db.session.query(Messages),
                           app_notifications=db.session.query(AppNotifications),
                           login_form=login_form,
                           user=user,
                           logged_in=logged_in)


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
    print("## Running Just-a-Dash routes.py directly. ##")
