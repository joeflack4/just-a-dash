"""Routes."""
from flask import render_template, url_for, redirect, request
# from flask.ext.login import current_user
from flask.ext.login import login_required

from justadash import app
# from justadash import db
# from justadash.models import Messages, AppNotifications
# from justadash.forms import RegisterForm
from justadash.forms import LoginForm
from justadash.includes import get_app_settings


##############
# - App Core - Root Pathing
@app.route('/')
def root_path():
    """Root path."""
    if True:
        # if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('welcome'))


@app.route('/welcome')
def welcome():
    """Welcome."""
    # logged_in = current_user.is_authenticated
    login_form = LoginForm(request.form)
    # register_form = RegisterForm(request.form)

    return render_template(
        'core_modules/welcome/index.html',
        module_name=get_app_settings('App Short-Title') + " Control Panel",
        page_name="Welcome",
        icon="fa fa-star-o",
        module_abbreviation="Home",
        app_config_settings=[],
        messages=[],
        notifications=[],
        login_form=login_form,
        current_user='Joe',
        logged_in=True)
    # app_config_settings=get_app_settings(),
    # messages=db.session.query(Messages),
    # notifications=db.session.query(AppNotifications),
    # login_form=login_form,
    # register_form=register_form,
    # current_user=current_user,
    # logged_in=logged_in)


@app.route('/index')
@login_required
def index():
    """Index."""
    # logged_in = current_user.is_authenticated
    login_form = LoginForm(request.form)
    return render_template(
        'core_modules/dashboard/index.html',
        module_name=get_app_settings('App Short-Title') + " Control Panel",
        page_name="Dashboard",
        icon="fa fa-dashboard",
        module_abbreviation="Home",
        app_config_settings=[],
        messages=[],
        notifications=[],
        login_form=login_form,
        current_user='Joe',
        logged_in=True)
    # app_config_settings=get_app_settings(),
    # messages=db.session.query(Messages),
    # notifications=db.session.query(AppNotifications),
    # login_form=login_form,
    # current_user=current_user,
    # logged_in=logged_in)
