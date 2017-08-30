from functools import wraps
from flask import request, redirect, flash
from flask.ext.login import current_user

# - Note: This code doesn't seem to work.
# from .forms import LoginForm
# def use_commmon_route_variables(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         logged_in = current_user.is_authenticated
#         login_form = LoginForm(request.form)
#     return wrap


def app_basic_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        permissions_type = 'administrative'
        if current_user.admin_role == 'basic' or current_user.admin_role == 'super' \
                or current_user.admin_role == 'master':
            return f(*args, **kwargs)
        else:
            flash('You do not have sufficient {} permissions to access this area.'.format(permissions_type), 'warning')
            return redirect(request.referrer)
    return wrap


def app_super_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        permissions_type = 'administrative'
        if current_user.admin_role == 'super' or current_user.admin_role == 'master':
            return f(*args, **kwargs)
        else:
            flash('You do not have sufficient {} permissions to access this area.'.format(permissions_type), 'warning')
            return redirect(request.referrer)
    return wrap


def app_master_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        permissions_type = 'administrative'
        if current_user.admin_role == 'master':
            return f(*args, **kwargs)
        else:
            flash('You do not have sufficient {} permissions to access this area.'.format(permissions_type), 'warning')
            return redirect(request.referrer)
    return wrap


def oms_basic_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        permissions_type = 'operations management'
        if current_user.oms_role == 'basic' or current_user.oms_role == 'super' or current_user.oms_role == 'master':
            return f(*args, **kwargs)
        else:
            flash('You do not have sufficient {} permissions to access this area.'.format(permissions_type), 'warning')
            return redirect(request.referrer)
    return wrap


def oms_super_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        permissions_type = 'operations management'
        if current_user.oms_role == 'super' or current_user.oms_role == 'master':
            return f(*args, **kwargs)
        else:
            flash('You do not have sufficient {} permissions to access this area.'.format(permissions_type), 'warning')
            return redirect(request.referrer)
    return wrap


def crm_basic_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        permissions_type = 'customer relations management'
        if current_user.crm_role == 'basic' or current_user.crm_role == 'super' or current_user.crm_role == 'master':
            return f(*args, **kwargs)
        else:
            flash('You do not have sufficient {} permissions to access this area.'.format(permissions_type), 'warning')
            return redirect(request.referrer)
    return wrap


def crm_super_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        permissions_type = 'customer relations management'
        if current_user.crm_role == 'super' or current_user.crm_role == 'master':
            return f(*args, **kwargs)
        else:
            flash('You do not have sufficient {} permissions to access this area.'.format(permissions_type), 'warning')
            return redirect(request.referrer)
    return wrap


def hrm_basic_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        permissions_type = 'human resources management'
        if current_user.hrm_role == 'basic' or current_user.hrm_role == 'super' or current_user.hrm_role == 'master':
            return f(*args, **kwargs)
        else:
            flash('You do not have sufficient {} permissions to access this area.'.format(permissions_type), 'warning')
            return redirect(request.referrer)
    return wrap


def hrm_super_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        permissions_type = 'human resources management'
        if current_user.hrm_role == 'super' or current_user.hrm_role == 'master':
            return f(*args, **kwargs)
        else:
            flash('You do not have sufficient {} permissions to access this area.'.format(permissions_type), 'warning')
            return redirect(request.referrer)
    return wrap


def ams_basic_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        permissions_type = 'accounting management'
        if current_user.ams_role == 'basic' or current_user.ams_role == 'super' or current_user.ams_role == 'master':
            return f(*args, **kwargs)
        else:
            flash('You do not have sufficient {} permissions to access this area.'.format(permissions_type), 'warning')
            return redirect(request.referrer)
    return wrap


def ams_super_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        permissions_type = 'accounting management'
        if current_user.ams_role == 'super' or current_user.ams_role == 'master':
            return f(*args, **kwargs)
        else:
            flash('You do not have sufficient {} permissions to access this area.'.format(permissions_type), 'warning')
            return redirect(request.referrer)
    return wrap


def mms_basic_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        permissions_type = 'marketing management'
        if current_user.mms_role == 'basic' or current_user.mms_role == 'super' or current_user.mms_role == 'master':
            return f(*args, **kwargs)
        else:
            flash('You do not have sufficient {} permissions to access this area.'.format(permissions_type), 'warning')
            return redirect(request.referrer)
    return wrap


def mms_super_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        permissions_type = 'marketing management'
        if current_user.mms_role == 'super' or current_user.mms_role == 'master':
            return f(*args, **kwargs)
        else:
            flash('You do not have sufficient {} permissions to access this area.'.format(permissions_type), 'warning')
            return redirect(request.referrer)
    return wrap
