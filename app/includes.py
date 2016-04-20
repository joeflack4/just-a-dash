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
    def get_columns(self, rows):
        columns = []
        for key in rows[0]:
            columns.append(key)
        return columns

    def __init__(self, data):
        self.data = json.loads(data)
        self.rows = self.data
        self.columns = self.get_columns(rows=self.rows)

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


def make_string_list(list):
    string = ''
    for item in list:
        string += item + ', '
    string = string[:-2]
    return string


def check_for_missing_required_columns(db_columns, import_data_columns):
    missing_columns = []
    for column in db_columns:
        if column['required'] == True:
            if column['name'] not in import_data_columns:
                missing_columns.append(column['name'])
    missing_columns = make_string_list(missing_columns)
    return missing_columns


def check_for_unknown_columns(db_columns, import_data_columns):
    unknown_columns = []
    for imported_column in import_data_columns:
        recognized_column = False
        for db_column in db_columns:
            if imported_column == db_column['name']:
                recognized_column = True
                break
        if recognized_column == False:
            unknown_columns.append(imported_column)
    unknown_columns = make_string_list(unknown_columns)
    return unknown_columns


def check_for_missing_optional_columns(db_columns, import_data_columns):
    missing_columns = []
    for column in db_columns:
        if column['name'] not in import_data_columns:
            missing_columns.append(column['name'])
    missing_columns = make_string_list(missing_columns)
    return missing_columns


def validate_columns(import_data, data_context):
    db_columns = []
    # - Determine columns based on context
    if data_context == 'User-CSV-Upload-Submit':
        db_columns = User.db_columns
    elif data_context == 'Customer-CSV-Upload-Submit':
        db_columns = Customers.db_columns
    elif data_context == 'Personnel-CSV-Upload-Submit':
        db_columns = Personnel.db_columns
    else:
        flash('Error in validation. Upload was detected, but could not determine the source. Please contact the '
              'application administrator for assistance.', 'danger')

    if db_columns != []:
        # - Column validation - Required & Unknown columns.
        missing_required_columns = check_for_missing_required_columns(db_columns, import_data.columns)
        unknown_columns = check_for_unknown_columns(db_columns, import_data.columns)
        if missing_required_columns != '' or unknown_columns != '':
            if missing_required_columns != '':
                error_message = Markup(
                    '<strong>Import Error: Missing Required columns</strong>. Tried to import data, but the following required ' \
                    'columns appear to have been missing from your import: <strong>{}</strong>'.format(
                        missing_required_columns) + \
                    '. Please correct the issue, and try again.')
                flash(error_message, 'danger')
            if unknown_columns != '':
                error_message = Markup(
                    '<strong>Import Error: Unrecognized Columns</strong>. Tried to import data, but some columns were not ' \
                    'recognized. Those columns were as follows: <strong>{}</strong>'.format(unknown_columns) + \
                    '. Please correct the issue, and try again.')
                flash(error_message, 'danger')
            return redirect(request.referrer)

        # - Column validation - Missing optional columns.
        missing_columns = check_for_missing_optional_columns(db_columns, import_data.columns)
        if missing_columns != '':
            message = Markup('During import, it was determined that some optional columns were not included. Those ' \
                             'columns were as follows: <strong>{}</strong>'.format(
                missing_columns) + '. The rest of the data, '
                                   'however, was included for processing as normal.')
            flash(message, 'info')


def assess_import_permissions(current_user, import_data, data_context):
    authority = True
    for row in import_data.rows:
        authority = check_permissions_to_assign_user_role(row, current_user)
        if authority == False:
            break
    return authority


# To do: validate each row. Add to erroneous/valid rows as necessary.
# This is going to be the hard part, I think, as I'm going to have to call upon regexp functions for each column.
def validate_rows(import_data, data_context):
    rows = {'erroneous_rows': [], 'valid_rows': []}
    # debugging - not iteratable
    # for row in import_data.rows:
    #     #NEEDS WORK -- try form.validate_on_submit()?
    #
    #     return

    return rows


def validate_import(current_user, import_data, data_context):
    validate_columns(import_data, data_context)
    authority = assess_import_permissions(current_user, import_data, data_context)

    if authority == True:
        rows = validate_rows(import_data, data_context)

        erroneous_rows = rows['erroneous_rows']
        if erroneous_rows != []:
            erroneous_row_string = ''
            for row in erroneous_rows:
                erroneous_row_string += str(row) + '\n'
            erroneous_row_string = erroneous_row_string[:-1]
            flash('Some rows did not pass validation, and were not imported. Please correct the following rows, and try '
                  'importing again:\n\n' + erroneous_row_string, 'danger')

        valid_rows = rows['valid_rows']
        return valid_rows
    elif authority == False:
        return redirect(request.referrer)
    else:
        flash('An unknown error occurred while trying to assess user permissions. Please contact the application '
              'administrator.', 'danger')
        redirect(request.referrer)


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


def check_permissions_to_assign_user_role(table, current_user):
    role_authority = {}
    non_authority_count = 0
    role_values_to_assign = {}
    role_fields = ('admin_role', 'oms_role', 'crm_role', 'hrm_role', 'ams_role', 'mms_role')
    role_assignments_denied = []

    # The following will work if authorizing a form submission.
    try:
        for field in table.data:
            if field in role_fields:
                role_values_to_assign[field] = table.data[field]
    # The following will work if authorizing a .csv upload.
    except:
        for field in table:
            if field in role_fields:
                role_values_to_assign[field] = table[field]

    for role, value in role_values_to_assign.items():
        if value != 'null':
            case_authority = current_user.check_administrative_authority(role, value)
            role_authority[role] = case_authority

    for role in role_authority:
        if role_authority[role] == False:
            role_assignments_denied.append(role)
            non_authority_count += 1
    role_assignments_denied = make_string_list(role_assignments_denied)

    if non_authority_count == 0:
        authority = True
    else:
        authority = False
        error_message = Markup('Permission denied to grant 1 or more user(s) permissions of the following type: '
            '<strong>{}</strong>'.format(role_assignments_denied) + '. It is not possible to assign administrative '
            'permissions greater or equal to one\'s own. Please locate the user(s) for whom this exception was caused, '
            'and please select lower permission(s).')
        flash(error_message, 'danger')

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
