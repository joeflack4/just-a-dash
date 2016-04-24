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
from validate_email import validate_email


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
    for column, metadata in db_columns.items():
        if metadata['required'] == True:
            if column not in import_data_columns:
                missing_columns.append(column)
    missing_columns = make_string_list(missing_columns)
    return missing_columns


def check_for_unknown_columns(db_columns, import_data_columns):
    unknown_columns = []
    for imported_column in import_data_columns:
        recognized_column = False
        for db_column in db_columns:
            if imported_column == db_column:
                recognized_column = True
                break
        if recognized_column == False:
            unknown_columns.append(imported_column)
    unknown_columns = make_string_list(unknown_columns)
    return unknown_columns


def check_for_missing_optional_columns(db_columns, import_data_columns):
    missing_columns = []
    for column, metadata in db_columns.items():
        if column not in import_data_columns:
            missing_columns.append(column)
    missing_columns = make_string_list(missing_columns)
    return missing_columns


def get_cols_from_context(data_context):
    db_columns = []
    if data_context == 'User-CSV-Upload-Submit':
        db_columns = User.db_columns
    elif data_context == 'Customer-CSV-Upload-Submit':
        db_columns = Customers.db_columns
    elif data_context == 'Personnel-CSV-Upload-Submit':
        db_columns = Personnel.db_columns
    else:
        flash('Error in validation. Upload was detected, but could not determine the source. Please contact the '
              'application administrator for assistance.', 'danger')
    return db_columns


def validate_columns(import_data, data_context):
    valid_schema = True
    db_columns = get_cols_from_context(data_context)
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
            valid_schema = False
            # Debugging - I want this to cancel function calls and simply redirect.
            # redirect(request.referrer)

        # - Column validation - Missing optional columns.
        missing_columns = check_for_missing_optional_columns(db_columns, import_data.columns)
        if missing_columns != '':
            message = Markup('During import, it was determined that some optional columns were not included. Those ' \
                             'columns were as follows: <strong>{}</strong>'.format(
                             missing_columns) + '. The rest of the data, however, was included for processing as normal.')
            flash(message, 'info')
    return valid_schema


def assess_import_permissions(current_user, import_data, data_context):
    authority = True
    for row in import_data.rows:
        authority = check_permissions_to_assign_user_role(row, current_user)
        if authority == False:
            break
    return authority


# To do: validate each row. Add to erroneous/valid rows as necessary.
# This is going to be the hard part, I think, as I'm going to have to call upon regexp functions for each column.
def validate_field(key, val, db_columns):
    validity = True
    validators = db_columns[key]['validators']
    validator_parameters = db_columns[key]['validator_parameters']
    errors = ''

    if validators == 'email':
        validity = validate_email(val)
        if validity == False:
            errors = key.capitalize() + ' field is not valid.'
    elif validators == 'selection':
        key.lower()
        if key in validator_parameters == False:
            validity = False
            errors = key.capitalize() + ' field not recognized as a valid selection.'
    elif validators == 'string':
        if validator_parameters['max']:
            if len(val) > validator_parameters['max']:
                validity = False
                errors = key.capitalize() + ' field has too many characters.'
        if validator_parameters['min']:
            if len(val) < validator_parameters['min']:
                validity = False
                errors = key.capitalize() + ' field has too few characters.'

    return validity, errors


def validate_rows(import_data, data_context):
    db_columns = get_cols_from_context(data_context)
    rows = {'erroneous_rows': [], 'valid_rows': []}

    for row in import_data.rows:
        error_count = 0
        for key, val in row.items():
            validity, errors = validate_field(key, val, db_columns)
            if validity == True:
                continue
            elif validity == False:
                error_count += 1
                erroneous_row = {}
                erroneous_row['row_data'] = row
                erroneous_row['errors'] = errors
                rows['erroneous_rows'].append(erroneous_row)
        if error_count == 0:
            rows['valid_rows'].append(row)

    return rows


def validate_import(current_user, import_data, data_context):
    # validate_columns(import_data, data_context)
    authority = True
    if data_context == 'User-CSV-Upload-Submit':
        authority = assess_import_permissions(current_user, import_data, data_context)

    if authority == True:
        rows = validate_rows(import_data, data_context)

        erroneous_rows = rows['erroneous_rows']
        if erroneous_rows != []:
            erroneous_row_string = ''
            i = 1
            for erroneous_row in erroneous_rows:
                erroneous_row_string += '<span style="text-decoration: underline">Row ' + str(i) + ': ' + \
                    str(erroneous_row['errors']) + '</span><br/>' + str(erroneous_row['row_data']) + '<br/><br/>'
                i += 1
            erroneous_row_string = erroneous_row_string[:-1]
            error_message = Markup('<strong>Import Error: Validation</strong>. Some rows did not pass validation, and were not imported. Please correct the following rows, and try '
                                   'importing again: <br/><br/>'+ erroneous_row_string)
            flash(error_message, 'danger')
            redirect(request.referrer)

        valid_rows = rows['valid_rows']
        return valid_rows

    elif authority == False:
        redirect(request.referrer)

    else:
        flash('An unknown error occurred while trying to assess user permissions. Please contact the application '
              'administrator.', 'danger')
        redirect(request.referrer)


def add_to_db(data_to_add, data_context):
    errors = []
    if data_context == 'User-CSV-Upload-Submit':
        for row in data_to_add:
            try:
                db.session.add(User(username=row['username'], email=row['email'], password=row['password'],
                                    admin_role=row['admin_role'], oms_role=row['oms_role'], crm_role=row['crm_role'],
                                    hrm_role=row['hrm_role'], ams_role=row['ams_role'], mms_role=row['mms_role']))
                db.session.commit()
            except:
                db.session.rollback()
                errors.append(row)
                # error_message = Markup('<strong>DB Import Error:</strong> We\'re sorry, but an unexpected error '
                #     'occurred while attempting to add records to the database. Please contact the application administrator.')
                # flash(error_message, 'danger')
    elif data_context == 'Customers-CSV-Upload-Submit':
        for row in data_to_add:
            try:
                # Need to flesh out either more parameters, or *args.
                db.session.add(Customers(name_last=row['name_last'], name_first=row['name_first']))
                db.session.commit()
            except:
                db.session.rollback()
                errors.append(row)
                # flash('Validation error occurred. Make sure data is valid for all rows, and try uploading again.',
                #       'danger')
    elif data_context == 'Personnel-CSV-Upload-Submit':
        for row in data_to_add:
            try:
                # Need to flesh out either more parameters, or *args.
                db.session.add(Personnel(name_last=row['name_last']))
                db.session.commit()
            except:
                db.session.rollback()
                errors.append(row)
                # flash('Validation error occurred. Make sure data is valid for all rows, and try uploading again.',
                #       'danger')
    else:
        flash('Error occurred when attempting to import data. Upload was detected, but could not determine the source. '
              'Please contact the application administrator.', 'danger')

    if errors:
        if errors != []:
            record_errors = ''
            for error in errors:
                record_errors += str(error) + '<br/>'
            error_message = Markup('<strong>DB Import Error:</strong> We\'re sorry, but an error occurred while '
                                   'attempting to add records to the database. The following entries were affected: '
                                   '<br/><br/>{}'.format(record_errors) + '<br/><br/>It is possible that the record(s) '
                                   'you are trying to add may already exist. If this is not the cae, please contact the '
                                   'application administrator.')
            flash(error_message, 'danger')


# -- App Settings
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
        flash('An error occurred while trying to delete user. User may not exist or otherwise already be deleted. If '
              'this is not the case, please contact the application administrator.', 'danger')


# -- Customer Management
def add_customer(add_form):
    try:
        new_customer = Customers(
            name_last=add_form.name_last.data,
            name_first=add_form.name_first.data,
            phone1=add_form.phone1.data,
            email1=add_form.email1.data,
            name_prefix='',
            name_suffix='',
            name_middle='',
            email2='',
            phone2='',
            phone3='',
            phone4='',
            phone5='',
            pii_dob='',
            pii_other='',
            phi='',
            pfi='',
            address_street=add_form.address_street.data,
            address_suite=add_form.address_suite.data,
            address_city=add_form.address_city.data,
            address_state=add_form.address_state.data,
            address_county='',
            address_zip=add_form.address_zip.data,
            address_zip_extension=add_form.address_zip_extension.data,
            billing_method='',
            billing_frequency='',
            billing_relation_name='',
            billing_email='',
            billing_address_street='',
            billing_address_suite='',
            billing_address_state='',
            billing_address_county='',
            billing_address_zip='',
            billing_address_zip_extension='',
            billing_notes='',
            relation_1_name='',
            relation_1_role='',
            relation_2_name='',
            relation_2_role='',
            relation_3_name='',
            relation_3_role='',
            relation_4_name='',
            relation_4_role='',
            relation_5_name='',
            relation_5_role='',
            customer_type='',
            customer_type_id1='',
            customer_type_id2='',
            customer_type_id3='',
            service_1_id='',
            service_1_day='',
            service_1_hours='',
            service_1_type='',
            service_1_rate='',
            service_2_id='',
            service_2_day='',
            service_2_hours='',
            service_2_type='',
            service_2_rate='',
            service_3_id='',
            service_3_day='',
            service_3_hours='',
            service_3_type='',
            service_3_rate='',
            service_4_id='',
            service_4_day='',
            service_4_hours='',
            service_4_type='',
            service_4_rate='',
            service_5_id='',
            service_5_day='',
            service_5_hours='',
            service_5_type='',
            service_5_rate='',
            service_6_id='',
            service_6_day='',
            service_6_hours='',
            service_6_type='',
            service_6_rate='',
            notes_case='',
            notes_other='')
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer successfully added!', 'success')
    except:
        db.session.rollback()
        flash('Sorry! It seems an issue occurred while attempting to add customer to database. Please ensure that the '
              'customer does not already exist. If you feel this is in error, please contact the application '
              'administrator.', 'warning')


def update_customer(update_form):
    try:
        fields_to_update = {}

        customer_id = update_form.id.data
        customer = Customers.query.filter_by(id=customer_id)

        if update_form.name_last.data != customer.first().name_last:
            fields_to_update['name_last'] = update_form.name_last.data
        if update_form.name_first.data != customer.first().name_first:
            fields_to_update['name_first'] = update_form.name_first.data
        if update_form.email1.data != customer.first().email1:
            fields_to_update['email1'] = update_form.email1.data
        if update_form.phone1.data != customer.first().phone1:
            fields_to_update['phone1'] = update_form.phone1.data
        if update_form.address_street.data != customer.first().address_street:
            fields_to_update['address_street'] = update_form.address_street.data
        if update_form.address_suite.data != customer.first().address_suite:
            fields_to_update['address_suite'] = update_form.address_suite.data
        if update_form.address_city.data != customer.first().address_city:
            fields_to_update['address_city'] = update_form.address_city.data
        if update_form.address_state.data != customer.first().address_state:
            fields_to_update['address_state'] = update_form.address_state.data
        if update_form.address_zip.data != customer.first().address_zip:
            fields_to_update['address_zip'] = update_form.address_zip.data
        if update_form.address_zip_extension.data != customer.first().address_zip_extension:
            fields_to_update['address_zip_extension'] = update_form.address_zip_extension.data

        if len(fields_to_update) == 0:
            flash('No changes to user were detected in form submission. Customer has been left unchanged.', 'info')
        else:
            customer.update(dict(fields_to_update))
            db.session.commit()
            flash('Customer successfully updated!', 'success')
    except:
        db.session.rollback()
        flash('Sorry! It seems an issue occurred while attempting to add/update customer. Please contact the application'
              ' administrator.', 'warning')


def delete_customer(update_form):
    customer_id = update_form.id.data
    customer = Customers.query.filter_by(id=customer_id)
    try:
        customer.delete()
        db.session.commit()
        flash('Customer successfully deleted!', 'success')
    except:
        db.session.rollback()
        flash(customer.id)
        flash('An error occurred while trying to delete customer. User may not exist or otherwise already be deleted. '
              'If this is not the case, please contact the application administrator.', 'danger')


# -- Personnel Management
def add_personnel(add_form):
    try:
        new_personnel = Personnel(
            name_last=add_form.name_last.data,
            name_first=add_form.name_first.data,
            phone1=add_form.phone1.data,
            email1=add_form.email1.data,
            name_prefix='',
            name_suffix='',
            name_middle='',
            email2='',
            phone2='',
            phone3='',
            phone4='',
            phone5='',
            pii_dob='',
            pii_other='',
            phi='',
            pfi='',
            address_street=add_form.address_street.data,
            address_suite=add_form.address_suite.data,
            address_city=add_form.address_city.data,
            address_state=add_form.address_state.data,
            address_county='',
            address_zip=add_form.address_zip.data,
            address_zip_extension=add_form.address_zip_extension.data,
            relation_1_name='',
            relation_1_notes='',
            relation_2_name='',
            relation_2_notes='',
            notes_other='')
        db.session.add(new_personnel)
        db.session.commit()
        flash('Personnel successfully added!', 'success')
    except:
        db.session.rollback()
        flash(
            'Sorry! It seems an issue occurred while attempting to add personnel to database. Please ensure that the '
            'personnel does not already exist. If you feel this is in error, please contact the application '
            'administrator.', 'warning')


def update_personnel(update_form):
    try:
        fields_to_update = {}

        personnel_id = update_form.id.data
        personnel = Personnel.query.filter_by(id=personnel_id)

        if update_form.name_last.data != personnel.first().name_last:
            fields_to_update['name_last'] = update_form.name_last.data
        if update_form.name_first.data != personnel.first().name_first:
            fields_to_update['name_first'] = update_form.name_first.data
        if update_form.email1.data != personnel.first().email1:
            fields_to_update['email1'] = update_form.email1.data
        if update_form.phone1.data != personnel.first().phone1:
            fields_to_update['phone1'] = update_form.phone1.data
            fields_to_update['address_street'] = update_form.address_street.data
        if update_form.address_suite.data != personnel.first().address_suite:
            fields_to_update['address_suite'] = update_form.address_suite.data
        if update_form.address_city.data != personnel.first().address_city:
            fields_to_update['address_city'] = update_form.address_city.data
        if update_form.address_state.data != personnel.first().address_state:
            fields_to_update['address_state'] = update_form.address_state.data
        if update_form.address_zip.data != personnel.first().address_zip:
            fields_to_update['address_zip'] = update_form.address_zip.data
        if update_form.address_zip_extension.data != personnel.first().address_zip_extension:
            fields_to_update['address_zip_extension'] = update_form.address_zip_extension.data

        if len(fields_to_update) == 0:
            flash('No changes to user were detected in form submission. Personnel has been left unchanged.', 'info')
        else:
            personnel.update(dict(fields_to_update))
            db.session.commit()
            flash('Personnel successfully updated!', 'success')
    except:
        db.session.rollback()
        flash('Sorry! It seems an issue occurred while attempting to add/update personnel. Please contact the application'
              ' administrator.', 'warning')


def delete_personnel(update_form):
    personnel_id = update_form.id.data
    personnel = Personnel.query.filter_by(id=personnel_id)
    try:
        personnel.delete()
        db.session.commit()
        flash('Personnel successfully deleted!', 'success')
    except:
        db.session.rollback()
        flash(personnel.id)
        flash('An error occurred while trying to delete personnel. User may not exist or otherwise already be deleted. '
              'If this is not the case, please contact the application administrator.', 'danger')
