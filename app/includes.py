# - Imports
import io
import csv
import json
from flask import flash, Markup, redirect, request
# from flask import url_for, make_response
from werkzeug.security import generate_password_hash
from app import db
# from requests import request
from .models import User, Customers, Personnel
# from .forms import UserAddForm


# - Variables


# - Classes
class Import_Data():
    data = {}
    columns = []
    rows = data

    def get_columns(self, data):
        columns = []
        column_row = data[0]
        for key, value in column_row:
            columns.append(key)
        return columns

    def __init__(self, data):
        self.data = data
        self.columns = self.get_columns(data)

    def __repr__(self):
        return '<Import Data of Schema: {}>'.format(self.columns)


# - Functions
# -- Shared Functions
def csv2json_conversion(file):
    # - Reference: Taken from https://gist.github.com/tonywhittaker/93fc9768fa135149edd3
    def csv2json(data):
        reader = csv.DictReader(data)
        out = json.dumps([row for row in reader])
        return out
    file_contents = io.StringIO(file)
    result = csv2json(file_contents)
    # - The following 3 lines are for contingent debugging purposes.
    # flash(result, 'info')
    # response = make_response(result)
    # response.headers["Content-Disposition"] = "attachment; filename=Converted.json"
    return result


def check_for_missing_required_columns(db_columns, import_data_columns):
    missing_required_columns = False
    for column in db_columns:
        if column['required'] == True:
            if import_data_columns[column] == False:
                missing_required_columns = True
                break
    return missing_required_columns


def check_for_unknown_columns(db_columns, import_data_columns):
    unknown_columns = ""
    for column in import_data_columns:
        if not db_columns[column]:
            unknown_columns += column + ', '
    return unknown_columns


def check_for_missing_columns(db_columns, import_data_columns):
    missing_columns = ""
    for column in db_columns:
            if import_data_columns[column] == False:
                missing_columns += column + ', '
    return missing_columns


# Need to list columns / required columns for the following 3 validation functions.
def validate_users(import_data):
    db_columns = [
        {'name': '', 'required': False},
    ]

    # - Column validation.
    missing_required_columns = check_for_missing_required_columns(db_columns, import_data.columns)
    if missing_required_columns == True:
        flash(
            'Error. Tried to import data, but required columns were missing. Please correct the issue, and try again.',
            'danger')
        return redirect(request.referrer)
    unknown_columns = check_for_unknown_columns(db_columns, import_data.columns)
    if unknown_columns != "":
        flash('Error. Tried to import data, but some columns were not recognized. Please correct the issue, and try '
              'again. Those columns were as follows: {}'.format(unknown_columns), 'info')
        return redirect(request.referrer)
    missing_columns = check_for_missing_columns(db_columns, import_data.columns)
    if missing_columns != "":
        flash('During import, it was determined that some optional columns were not included. Those columns were as '
              'follows: {}'.format(missing_columns), 'info')

    # - Row validation.
    # Perhaps reject whole .csv for now instead of returning a .csv of erroneous rows, for ease.
    erroneous_rows = []
    valid_rows = []
    # To do: validate each row. Add to erroneous/valid rows as necessary.
    # This is going to be the hard part, I think, as I'm going to have to call upon regexp functions for each column.

    return valid_rows


def validate_customers(import_data):
    db_columns = [
        {'name': '', 'required': False},
    ]

    # - Column validation.
    missing_required_columns = check_for_missing_required_columns(db_columns, import_data.columns)
    if missing_required_columns == True:
        flash('Error. Tried to import data, but required columns were missing. Please correct the issue, and try again.',
              'danger')
        return redirect(request.referrer)
    unknown_columns = check_for_unknown_columns(db_columns, import_data.columns)
    if unknown_columns != "":
        flash('Error. Tried to import data, but some columns were not recognized. Please correct the issue, and try '
              'again. Those columns were as follows: {}'.format(unknown_columns), 'info')
        return redirect(request.referrer)
    missing_columns = check_for_missing_columns(db_columns, import_data.columns)
    if missing_columns != "":
        flash('During import, it was determined that some optional columns were not included. Those columns were as '
              'follows: {}'.format(missing_columns), 'info')

    # - Row validation.
    # Perhaps reject whole .csv for now instead of returning a .csv of erroneous rows, for ease.
    erroneous_rows = []
    valid_rows = []
    # To do: validate each row. Add to erroneous/valid rows as necessary.
    # This is going to be the hard part, I think, as I'm going to have to call upon regexp functions for each column.

    return valid_rows


def validate_personnel(import_data):
    db_columns = [
        {'name': '', 'required': False},
    ]

    # - Column validation.
    missing_required_columns = check_for_missing_required_columns(db_columns, import_data.columns)
    if missing_required_columns == True:
        flash(
            'Error. Tried to import data, but required columns were missing. Please correct the issue, and try again.',
            'danger')
        return redirect(request.referrer)
    unknown_columns = check_for_unknown_columns(db_columns, import_data.columns)
    if unknown_columns != "":
        flash('Error. Tried to import data, but some columns were not recognized. Please correct the issue, and try '
              'again. Those columns were as follows: {}'.format(unknown_columns), 'info')
        return redirect(request.referrer)
    missing_columns = check_for_missing_columns(db_columns, import_data.columns)
    if missing_columns != "":
        flash('During import, it was determined that some optional columns were not included. Those columns were as '
              'follows: {}'.format(missing_columns), 'info')

    # - Row validation.
    # Perhaps reject whole .csv for now instead of returning a .csv of erroneous rows, for ease.
    erroneous_rows = []
    valid_rows = []
    # To do: validate each row. Add to erroneous/valid rows as necessary.
    # This is going to be the hard part, I think, as I'm going to have to call upon regexp functions for each column.

    return valid_rows

def validate_import(import_data, data_context):
    # To do: Update the below if statement to declare different 'db_columns', rather than calling a separate function.
    # , and just use that db_columns variable for the rest of this validation function.

    if data_context == '/user-management':
        validated_data = validate_users(import_data)
    elif data_context == '/crm':
        validated_data = validate_customers(import_data)
    elif data_context == '/hrm':
        validated_data = validate_personnel(import_data)
    else:
        validated_data = ''
        flash('Error in validation. Upload was detected, but could not determine the source. Please contact the '
              'application administrator for assistance.', 'danger')
    return validated_data


def add_to_db(data_to_add, data_context):
    error_message = ''
    errors = []
    # I think the below row.KEY is likely to cause problems. may need to do ['KEY'] instead for now, or otherwise
    # set up as a class.
    if data_context == '/user-management':
        for row in data_to_add.rows:
            try:
                db.session.add(User(username=row.username, email=row.email, password=row.password, admin_role=row.admin_role,
                                    oms_role=row.oms_role, crm_role=row.crm_role, hrm_role=row.hrm_role,
                                    ams_role=row.ams_role, mms_role=row.mms_role))
                db.session.commit()
            except:
                db.session.rollback()
                errors.append(row.username)
                flash('Validation error occurred. Make sure data is valid for all rows, and try uploading again.',
                      'danger')
    elif data_context == '/crm':
        for row in data_to_add.rows:
            try:
                # Need to flesh out either more parameters, or *args.
                db.session.add(Customers(name_last=row.name_last, name_first=row.name_first))
                db.session.commit()
            except:
                db.session.rollback()
                errors.append(row.name_last)
                flash('Validation error occurred. Make sure data is valid for all rows, and try uploading again.',
                      'danger')
    elif data_context == '/hrm':
        for row in data_to_add.rows:
            try:
                # Need to flesh out either more parameters, or *args.
                db.session.add(Personnel(name_last=row.name_last))
                db.session.commit()
            except:
                db.session.rollback()
                errors.append(row.name_last)
                flash('Validation error occurred. Make sure data is valid for all rows, and try uploading again.',
                      'danger')
    else:
        flash('Error occurred when attempting to import data. Upload was detected, but could not determine the source. '
              'Please contact the application administrator.', 'danger')

    if errors:
        if errors != []:
            for error in errors:
                error_message += error + ', '
        flash('Some issues occurred while trying to import data. The following entries were affected: {}'.format(error_message), 'danger')


# -- App Settings
def check_permissions_to_upload_data(current_user, validated_data, validation_context):
    return

def check_permissions_to_change_App_Naming_and_Aesthetics(current_user):
    return


def update_names_and_aesthetics(current_user):
    return


def check_permissions_to_change_App_Secret_Key(current_user):
    return


def update_secret_key(current_user):
    return


def check_permissions_to_change_App_Modules(current_user):
    return


def update_modules(current_user):
    return


# -- User Management
def add_user(add_form):
    try:
        new_user = User(
            username=add_form.username.data,
            email=add_form.email.data,
            password=add_form.password.data,
            admin_role=add_form.admin_role.data,
            oms_role=add_form.oms_role.data,
            crm_role=add_form.crm_role.data,
            hrm_role=add_form.hrm_role.data,
            ams_role=add_form.ams_role.data,
            mms_role=add_form.mms_role.data)
        db.session.add(new_user)
        db.session.commit()
        flash('User successfully added!', 'success')
    except:
        db.session.rollback()
        flash(
            'Sorry! It seems an issue occurred while attempting to add user to database. Please ensure that the username/e-mail is not already taken. If you feel this is in error, please contact the application administrator.',
            'warning')


def check_permissions_to_update_user(update_form, current_user):
    roles = ('admin_role', 'oms_role', 'crm_role', 'hrm_role', 'ams_role', 'mms_role')
    role_related_form_submissions = {}
    role_superiorities = {}
    inferiorities = ""

    try:
        for attr, value in update_form.__dict__.items():
            for role in roles:
                if role == attr:
                    role_related_form_submissions[attr] = value.data

        user_submitted_id = update_form.user_id.data
        user_to_compare = User.query.filter_by(id=user_submitted_id).first()
        for attr, value in user_to_compare.__dict__.items():
            for role in roles:
                if role == attr:
                    # The following conditional ignores role superiority assessment the the form field submission is
                    # 'null', which occurs when the field has been left blank. Otherwise, assesses role superiority.
                    if role_related_form_submissions[role] != 'null':
                        try:
                            role_superiority = current_user.check_administrative_superiority(role, role_value=value)
                            role_superiorities[role] = role_superiority
                        except:
                            flash('Permissions Assessment Error #1 - Authority to create, modify, or delete data could not be determined.', 'danger')

        for key, value in role_superiorities.items():
            if value == False:
                inferiorities += (key + " / ")
        # The following line formats the 'inferiorities' string.
        inferiorities = inferiorities[:-3]

    except:
        flash('Permissions Assessment Error #2 - An error occurred while trying to access form data.', 'danger')

    if inferiorities != "":
        flash(Markup('Permission denied for some field submissions. You have attempted to modify a user with '
                     '<strong>greater</strong> or <strong>equal</strong> administrative roles in the following modules: '
                     '<strong>{}</strong>.').format(inferiorities), 'danger')
        flash(Markup('<strong>Info!</strong> Only users with a greater administrative role in a particular category may '
                     'modify another users role in that particular category. '
                     'If this user must be modified, please only update role fields where you have administrative superiority. '
                     'If you do not, but feel that the user\'s role must still be updated, please consult with a user with superior permissions, '
                     'or request greater permissions for yourself.'), 'info')

    return role_superiorities


def check_permissions_to_assign_user_role(update_form, current_user):
    role_authority = {}
    non_authority_count = 0
    role_values_to_assign = {}

    for field in update_form.data:

        if field == ('admin_role' or 'oms_role' or 'crm_role' or 'hrm_role' or 'ams_role' or 'mms_role'):
            role_values_to_assign[field] = update_form.data[field]

        #DEBUGGING
        # authority = True

    # for role in role_values_to_assign:
    for role, value in role_values_to_assign.items():
        if value != 'null':
            #debugging
            flash(role)
            flash(value)
            # flash(role_values_to_assign[role])

            # case_authority = current_user.check_administrative_authority(role, role_values_to_assign[role])
            case_authority = current_user.check_administrative_authority(role, value)
            role_authority[role] = case_authority

    for role in role_authority:
        if role_authority[role] == False:
            non_authority_count += 1

    if non_authority_count == 0:
        authority = True
    else:
        authority = False
        flash('Permission denied. It is not possible to assign administrative permissions greater or equal to one\'s own.', 'danger')

    return authority


def update_user(update_form, role_superiorities):
    try:
        fields_to_update = {}

        user_id = update_form.user_id.data
        user = User.query.filter_by(id=user_id)

        if update_form.username.data != user.first().username:
            fields_to_update['username'] = update_form.username.data
        if update_form.email.data != user.first().email:
            fields_to_update['email'] = update_form.email.data
        if len(update_form.password.data) > 0:
            password = generate_password_hash(update_form.password.data)
            fields_to_update['password'] = password
        if update_form.admin_role.data != 'null':
            if role_superiorities['admin_role'] == True:
                fields_to_update['admin_role'] = update_form.admin_role.data
        if update_form.oms_role.data != 'null':
            if role_superiorities['oms_role'] == True:
                fields_to_update['oms_role'] = update_form.oms_role.data
        if update_form.crm_role.data != 'null':
            if role_superiorities['crm_role'] == True:
                fields_to_update['crm_role'] = update_form.crm_role.data
        if update_form.hrm_role.data != 'null':
            if role_superiorities['hrm_role'] == True:
                fields_to_update['hrm_role'] = update_form.hrm_role.data
        if update_form.ams_role.data != 'null':
            if role_superiorities['ams_role'] == True:
                fields_to_update['ams_role'] = update_form.ams_role.data
        if update_form.mms_role.data != 'null':
            if role_superiorities['mms_role'] == True:
                fields_to_update['mms_role'] = update_form.mms_role.data

        if len(fields_to_update) == 0:
            flash('No changes to user were detected in form submission. User has been left unchanged.', 'info')
        else:
            user.update(dict(fields_to_update))
            db.session.commit()
            flash('User successfully updated!', 'success')
    except:
        db.session.rollback()
        flash('Sorry! It seems an issue occurred while attempting to add/update user. Please contact the application administrator.', 'warning')


def check_permissions_to_delete_user(delete_form, current_user):
    try:
        user_submitted_id = delete_form.user_id.data
        user_to_compare = User.query.filter_by(id=user_submitted_id).first()
        try:
            superiority = current_user.check_administrative_superiority('admin_role', user_to_compare.admin_role)
        except:
            superiority = False
            flash('Permissions Assessment Error #1 - Authority to delete data could not be determined.', 'danger')
    except:
        superiority = False
        flash('Permissions Assessment Error #2 - An error occurred while trying to access form data.', 'danger')

    return superiority


def delete_user(update_form):
    user_id = update_form.user_id.data
    user = User.query.filter_by(id=user_id)
    try:
        user.delete()
        db.session.commit()
        flash('User successfully deleted!', 'success')
    except:
        db.session.rollback()
        flash(user.id)
        flash(
            'An error occurred while trying to delete user. User may not exist or otherwise already be deleted. If this is not the case, please contact the application administrator.',
            'danger')
