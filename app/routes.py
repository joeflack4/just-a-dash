from flask import render_template, url_for, flash, redirect, request, session
from flask.ext.login import login_user
from app import app, db, bcrypt
# Unused -> from flask_table import Table, Col
# from functools import wraps

from .models import User, Messages, Result

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
    from .forms import LoginForm, RegisterForm
    from flask.ext.login import login_required
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
    if 'logged_in' in session:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('welcome'))


@app.route('/welcome')
def welcome():
    form = LoginForm(request.form)
    register_form = RegisterForm()
    return render_template('core_modules/welcome/index.html',
                           module_name="Just-a-Dash Control Panel",
                           page_name="Welcome",
                           icon="fa fa-star-o",
                           module_abbreviation="Home",
                           messages=db.session.query(Messages),
                           form=form,
                           register_form=register_form)


@app.route('/index')
@app.route('/dashboard')
@app.route('/home')
@login_required
def index():
    username = ""
    form = LoginForm(request.form)
    return render_template('core_modules/dashboard/index.html',
                           module_name="Just-a-Dash Control Panel",
                           page_name="Dashboard",
                           icon="fa fa-dashboard",
                           module_abbreviation="Home",
                           username=username,
                           messages=db.session.query(Messages),
                           form=form)


################
# - Core Modules
@app.route('/account-settings')
@login_required
def account_settings():
    form = LoginForm(request.form)
    return render_template('core_modules/account_settings/index.html',
                           icon="fa fa-dashboard",
                           module_abbreviation="Account Settings",
                           module_name="Account Settings",
                           page_name="Account Settings Home",
                           messages=db.session.query(Messages),
                           form=form)


@app.route('/app-settings')
@login_required
def app_settings():
    form = LoginForm(request.form)
    return render_template('core_modules/app_settings/index.html',
                           icon="fa fa-dashboard",
                           module_abbreviation="App Settings",
                           module_name="App Settings",
                           page_name="App Settings Home",
                           messages=db.session.query(Messages),
                           form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', True)
    flash(u'Logged out. Thank you, come again!', 'success')
    return redirect(url_for('welcome'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = []
    form = LoginForm(request.form)
    register_form = RegisterForm()

    if request.method == 'POST':
        # if request.form['username'] == 'admin' or request.form['password'] == 'admin':
        if form.validate_on_submit():
            user = User.query.filter_by(username=request.form['username']).first()
            # DEBUGGING
            # flash('test')
            # user = User.query.filter_by(name=request.form['Username']).first()
            # login_user(user)
            # return redirect(url_for('index'))
            # DEBUGGING
            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                # session['logged_in'] = True
                login_user(user)
                flash(u'Logged in. Welcome back!', 'success')
                return redirect(url_for('index'))
        else:
            errors.append('Invalid credentials. Please try again.')
            user = User.query.filter_by(username=request.form['username']).first()
            # errors.append(request.form['username'])
            # errors.append(request.form['password'])
            for error in errors:
                flash(error, 'danger')
            return render_template('core_modules/login/index.html',
                                   icon="fa fa-dashboard",
                                   module_abbreviation="Home",
                                   module_name="Just-a-Dash Control Panel",
                                   page_name="Login",
                                   messages=db.session.query(Messages),
                                   form=form)
                                   # errors=errors)
                                   # login_form=form)
    else:
        return render_template('core_modules/login/index.html',
                                   icon="fa fa-dashboard",
                                   module_abbreviation="Home",
                                   module_name="Just-a-Dash Control Panel",
                                   page_name="Login",
                                   messages=db.session.query(Messages),
                                   form=form,
                                   register_form=register_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm(request.form)
    # if request.method == 'POST':
    #     flash(u'Thank you for your submission. The site administrator will contact you when registration is complete.', 'success')
    register_form = RegisterForm()
    if request.method == 'POST':
        if register_form.validate_on_submit():
            user = User(
                username=register_form.username.data,
                email=register_form.email.data,
                password=register_form.password.data
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(u'Registration complete! You have been logged in.', 'success')
            # return redirect(url_for('index'))
        else:
            flash(u'Registration failed. Please try again, or contact the site administrator. Ensure that: (1) Username is between 3-25 characters, (2) E-mail is between 6-40 characters, (3) Password is beteen 6-25 characters, (4) Password and confirm password are matching.', 'warning')

    return render_template('core_modules/register/index.html',
                           icon="fa fa-pencil-square-o",
                           module_abbreviation="Registration",
                           module_name="Registration",
                           page_name="New Submission",
                           messages=db.session.query(Messages),
                           form=form,
                           register_form=register_form)


@app.route('/profile')
@login_required
def profile():
    form = LoginForm(request.form)
    return render_template('core_modules/profile/index.html',
                           icon="fa fa-dashboard",
                           module_abbreviation="Profile",
                           module_name="Profile",
                           page_name="Profile Home",
                           messages=db.session.query(Messages),
                           form=form)


############
# - Modules
@app.route('/hr')
@app.route('/hrm')
@login_required
def hrm():
    form = LoginForm(request.form)
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
                               form=form)


@app.route('/crm')
@login_required
def crm():
    form = LoginForm(request.form)
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
                           form=form)


@app.route('/operations')
@login_required
def operations(*args):
    form = LoginForm(request.form)
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
                           form=form)


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
    form = LoginForm(request.form)
    return render_template('modules/accounting/index.html',
                           icon="fa fa-bar-chart",
                           module_abbreviation="AMS",
                           module_name="Accounting Management",
                           page_name="AMS Home",
                           messages=db.session.query(Messages),
                           form=form)


@app.route('/mms', methods=['GET', 'POST'])
@app.route('/marketing', methods=['GET', 'POST'])
@login_required
def marketing():
    errors = []
    results = {}
    form = LoginForm(request.form)
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
                                   form=form)

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
                    result_no_stop_words=no_stop_words_count
                )
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
                           form=form)


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
