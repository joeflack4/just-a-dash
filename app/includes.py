# - Imports
import io
import csv
import json
from flask import flash, Markup, redirect, request
# from flask import url_for, make_response
from werkzeug.security import generate_password_hash
from app import db
# from requests import request
from .models import User, AppConfig, OmsConfig, Customers, Personnel
from validate_email import validate_email


# - Variables


# - Classes
class Import_Data():
    formatted_rows = []

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

def format_phone_number(phone_number):
    if phone_number[:1] == 1:
        return phone_number
    else:
        return '1' + str(phone_number)


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
            errors = 'The <strong>' + key + '</strong> field was not recognized as a valid selection.'
    elif validators == 'string':
        try:
            if validator_parameters['max']:
                if len(val) > validator_parameters['max']:
                    validity = False
                    errors = 'The <strong>' + key + '</strong> field contained data (<strong>' + val + '</strong>) which exceeded the' \
                             ' maximum characters requirement of <strong>' + str(validator_parameters['max']) + '</strong>.'
        except KeyError:
            validity = True
        try:
            if validator_parameters['min']:
                if len(val) < validator_parameters['min']:
                    validity = False
                    errors = 'The <strong>' + key + '</strong> field contained data (<strong>' + val + '</strong>) which did not meet the' \
                             ' minimum characters requirement of <strong>' + str(validator_parameters['min']) + '</strong>.'
        except KeyError:
            validity = True

    return validity, errors


def validate_rows(import_data, data_context):
    db_columns = get_cols_from_context(data_context)
    rows = {'erroneous_rows': [], 'valid_rows': []}
    formatted_rows = []

    # Remove Empty Column(s)
    for row in import_data.rows:
        for key, val in row.items():
            if key == '':
                del row[key]
                break

    # Remove Columns with Empty Values
    for row in import_data.rows:
        formatted_row = {}
        for key, val in row.items():
            if val != '':
                formatted_row[key] = val
        formatted_rows.append(formatted_row)
    import_data.formatted_rows = formatted_rows

    # Separate Valid/Erroneous Rows
    # for row in import_data.rows:
    for row in import_data.formatted_rows:
        error_count = 0
        for key, val in row.items():
            if key != '':
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
    authority = True
    if data_context == 'User-CSV-Upload-Submit':
        authority = assess_import_permissions(current_user, import_data, data_context)

    if authority == True:
        rows = validate_rows(import_data, data_context)
        erroneous_rows = rows['erroneous_rows']

        # Display errors.
        if len(erroneous_rows) > 0:
            erroneous_row_string = '<ul>'
            i = 1

            for erroneous_row in erroneous_rows:
                erroneous_row_string += '<li>Row ' + str(i) + ': ' + \
                    str(erroneous_row['errors']) + '</li>'
                i += 1
            erroneous_row_string = erroneous_row_string[:-1]
            erroneous_row_string += '</ul>'
            error_message = Markup('<strong>Import Error: Validation</strong>. Some rows did not pass validation, and '
                                   'thus no data has been imported. Please correct the following rows, and try '
                                   'importing again: <br/><br/>'+ erroneous_row_string)

            # - Error Handling: Unfortunately, Flask's 'flash()' functionality will fail silently and display nothing if
            # there is/are flashed message(s) which exceed a certain amount of characters. In personal trials, the
            # maximum amount that I was able to successfully display was somewhere between a successful error message
            # of '68,493' characters, and a silent error of a message containing '91,326' characters.
            if len(error_message) > 68493:
                error_message = Markup('<strong>Import Error: Validation</strong>. Some rows did not pass validation, '
                                       'and thus no data has been imported. Please ensure that all fields meet the '
                                       'required constraints.')

            flash(error_message, 'danger')
            redirect(request.referrer)

        # Return valid rows.
        valid_rows = rows['valid_rows']
        return valid_rows

    elif authority == False:
        flash('You do not have sufficient permissions to import this data.', 'warning')
        redirect(request.referrer)

    else:
        flash('An unknown error occurred while trying to assess user permissions. Please contact the application '
              'administrator.', 'danger')
        redirect(request.referrer)


# - Note: Currently unused. To handle possible KeyError exceptions, using row.get('key') instead of new_cell(row['key'])
def new_cell(data):
    try:
        return data
    except KeyError:
        return ''


def add_to_db(data_to_add, data_context):
    errors = []
    i = 1

    if data_context == 'User-CSV-Upload-Submit':
        for row in data_to_add:
            i += 1
            try:
                db.session.add(User(username=row.get('username'),
                                    email=row.get('email'),
                                    password=row.get('password'),
                                    admin_role=row.get('admin_role'),
                                    oms_role=row.get('oms_role'),
                                    crm_role=row.get('crm_role'),
                                    hrm_role=row.get('hrm_role'),
                                    ams_role=row.get('ams_role'),
                                    mms_role=row.get('mms_role')
                                    ))
                db.session.commit()
            except:
                db.session.rollback()
                errors.append(i)

    elif data_context == 'Customer-CSV-Upload-Submit':

        # - DEBUGGING
        # flash(new_cell(data_to_add[0]['name_last']))
        # flash(new_cell(data_to_add[0]['name_first']))
        # flash(new_cell(data_to_add[0].get('name_prefix')))
        # upload_test = ['name_last', 'name_first', 'name_prefix', 'name_suffix', 'name_middle', 'email1', 'email2', 'phone1', 'phone2',
        #         'phone3', 'phone4', 'phone5', 'pii_dob', 'pii_other', 'phi', 'pfi', 'address_street',
        #         'address_suite', 'address_city',
        #         'address_state', 'address_county', 'address_zip', 'address_zip_extension', 'billing_method',
        #         'billing_frequency',
        #         'billing_relation_name', 'billing_email', 'billing_address_street', 'billing_address_suite',
        #         'billing_address_state', 'billing_address_county', 'billing_address_city', 'billing_address_zip',
        #         'billing_address_zip_extension',
        #         'billing_notes', 'relation_1_name', 'relation_1_role', 'relation_2_name', 'relation_2_role',
        #         'relation_3_name',
        #         'relation_3_role', 'relation_4_name', 'relation_4_role', 'relation_5_name', 'relation_5_role',
        #         'customer_type',
        #         'customer_type_id1', 'customer_type_id2', 'customer_type_id3', 'service_1_id', 'service_1_day',
        #         'service_1_hours',
        #         'service_1_type', 'service_1_rate', 'service_2_id', 'service_2_day', 'service_2_hours',
        #         'service_2_type',
        #         'service_2_rate', 'service_3_id', 'service_3_day', 'service_3_hours', 'service_3_type',
        #         'service_3_rate',
        #         'service_4_id', 'service_4_day', 'service_4_hours', 'service_4_type', 'service_4_rate', 'service_5_id',
        #         'service_5_day', 'service_5_hours', 'service_5_type', 'service_5_rate', 'service_6_id', 'service_6_day',
        #         'service_6_hours', 'service_6_type', 'service_6_rate', 'notes_case', 'notes_other']
        # - DEBUGGING




        for row in data_to_add:
            i += 1
            try:
                # Need to flesh out either more parameters, or *args.
                # Debugging
                # for item in upload_test:
                #     db.session.add(Customers(item=row.get('item'))
                # Debugging
                db.session.add(Customers(name_last=row.get('name_last'),
                                         name_first=row.get('name_first'),
                                         name_prefix=row.get('name_prefix'),
                                         name_suffix=row.get('name_suffix'),
                                         name_middle=row.get('name_middle'),
                                         email1=row.get('email1'),
                                         email2=row.get('email2'),
                                         phone1=row.get('phone1'),
                                         phone2=row.get('phone2'),
                                         phone3=row.get('phone3'),
                                         phone4=row.get('phone4'),
                                         phone5=row.get('phone5'),
                                         pii_dob=row.get('pii_dob'),
                                         pii_other=row.get('pii_other'),
                                         phi=row.get('phi'),
                                         pfi=row.get('pfi'),
                                         address_street=row.get('address_street'),
                                         address_suite=row.get('address_suite'),
                                         address_city=row.get('address_city'),
                                         address_state=row.get('address_state'),
                                         address_county=row.get('address_county'),
                                         address_zip=row.get('address_zip'),
                                         address_zip_extension=row.get('address_zip_extension'),
                                         billing_method=row.get('billing_method'),
                                         billing_frequency=row.get('billing_frequency'),
                                         billing_relation_name=row.get('billing_relation_name'),
                                         billing_email=row.get('billing_email'),
                                         billing_address_street=row.get('billing_address_street'),
                                         billing_address_suite=row.get('billing_address_suite'),
                                         billing_address_state=row.get('billing_address_state'),
                                         billing_address_city=row.get('billing_address_city'),
                                         billing_address_county=row.get('billing_address_county'),
                                         billing_address_zip=row.get('billing_address_zip'),
                                         billing_address_zip_extension=row.get('billing_address_zip_extension'),
                                         billing_notes=row.get('billing_notes'),
                                         relation_1_name=row.get('relation_1_name'),
                                         relation_1_role=row.get('relation_1_role'),
                                         relation_2_name=row.get('relation_2_name'),
                                         relation_2_role=row.get('relation_2_role'),
                                         relation_3_name=row.get('relation_3_name'),
                                         relation_3_role=row.get('relation_3_role'),
                                         relation_4_name=row.get('relation_4_name'),
                                         relation_4_role=row.get('relation_4_role'),
                                         relation_5_name=row.get('relation_5_name'),
                                         relation_5_role=row.get('relation_5_role'),
                                         customer_type=row.get('customer_type'),
                                         customer_type_id1=row.get('customer_type_id1'),
                                         customer_type_id2=row.get('customer_type_id2'),
                                         customer_type_id3=row.get('customer_type_id3'),
                                         service_1_id=row.get('service_1_id'),
                                         service_1_day=row.get('service_1_day'),
                                         service_1_hours=row.get('service_1_hours'),
                                         service_1_type=row.get('service_1_type'),
                                         service_1_rate=row.get('service_1_rate'),
                                         service_2_id=row.get('service_2_id'),
                                         service_2_day=row.get('service_2_day'),
                                         service_2_hours=row.get('service_2_hours'),
                                         service_2_type=row.get('service_2_type'),
                                         service_2_rate=row.get('service_2_rate'),
                                         service_3_id=row.get('service_3_id'),
                                         service_3_day=row.get('service_3_day'),
                                         service_3_hours=row.get('service_3_hours'),
                                         service_3_type=row.get('service_3_type'),
                                         service_3_rate=row.get('service_3_rate'),
                                         service_4_id=row.get('service_4_id'),
                                         service_4_day=row.get('service_4_day'),
                                         service_4_hours=row.get('service_4_hours'),
                                         service_4_type=row.get('service_4_type'),
                                         service_4_rate=row.get('service_4_rate'),
                                         service_5_id=row.get('service_5_id'),
                                         service_5_day=row.get('service_5_day'),
                                         service_5_hours=row.get('service_5_hours'),
                                         service_5_type=row.get('service_5_type'),
                                         service_5_rate=row.get('service_5_rate'),
                                         service_6_id=row.get('service_6_id'),
                                         service_6_day=row.get('service_6_day'),
                                         service_6_hours=row.get('service_6_hours'),
                                         service_6_type=row.get('service_6_type'),
                                         service_6_rate=row.get('service_6_rate'),
                                         notes_case=row.get('notes_case'),
                                         notes_other=row.get('notes_other')
                                         ))
                db.session.commit()
            except:
                db.session.rollback()
                errors.append(i)

    elif data_context == 'Personnel-CSV-Upload-Submit':
        for row in data_to_add:
            i += 1
            try:
                # Need to flesh out either more parameters, or *args.
                db.session.add(Personnel(name_last=row.get('name_last'),
                                         name_first=row.get('name_first'),
                                         name_prefix=row.get('name_prefix'),
                                         name_suffix=row.get('name_suffix'),
                                         name_middle=row.get('name_middle'),
                                         email1=row.get('email1'),
                                         email2=row.get('email2'),
                                         phone1=row.get('phone1'),
                                         phone2=row.get('phone2'),
                                         phone3=row.get('phone3'),
                                         phone4=row.get('phone4'),
                                         phone5=row.get('phone5'),
                                         pii_dob=row.get('pii_dob'),
                                         pii_other=row.get('pii_other'),
                                         phi=row.get('phi'),
                                         pfi=row.get('pfi'),
                                         address_street=row.get('address_street'),
                                         address_suite=row.get('address_suite'),
                                         address_city=row.get('address_city'),
                                         address_state=row.get('address_state'),
                                         address_county=row.get('address_county'),
                                         address_zip=row.get('address_zip'),
                                         address_zip_extension=row.get('address_zip_extension'),
                                         relation_1_name=row.get('relation_1_name'),
                                         relation_1_notes=row.get('relation_1_notes'),
                                         relation_2_name=row.get('relation_2_name'),
                                         relation_2_notes=row.get('relation_2_notes'),
                                         notes_other=row.get('notes_other')
                                         ))
                db.session.commit()
            except:
                db.session.rollback()
                errors.append(i)

    else:
        flash('Error occurred when attempting to import data. Upload was detected, but could not determine the source. '
              'Please contact the application administrator.', 'danger')

    if errors:
        if len(errors) > 0:
            record_errors = ''
            for error in errors:
                record_errors += str(error) + ', '
            error_message = Markup('<p><strong>DB Import Error:</strong> We\'re sorry, but an error occurred while '
                                   'attempting to add records to the database.</p><p>The following row #\'s were affected (header row being row #1): '
                                   '{}'.format(record_errors) + '</p><p>It is possible that the record(s) '
                                   'you are trying to add may already exist. If this is not the case, please contact the '
                                   'application administrator.')
            flash(error_message, 'danger')


# -- App Settings
def get_app_settings(*args):
    if not args:
        try:
            app_config_settings = {'App Icon': AppConfig.query.filter_by(key='App Icon').first().value,
                                   'App Name': AppConfig.query.filter_by(key='App Name').first().value,
                                   'App Short-Title': AppConfig.query.filter_by(key='App Short-Title').first().value,
                                   'App Title': AppConfig.query.filter_by(key='App Title').first().value,
                                   'Secret Key': AppConfig.query.filter_by(key='Secret Key').first().value,
                                   'Toggle Placeholders': AppConfig.query.filter_by(key='Toggle Placeholders').first().value,}
        except:
            app_config_settings = False
        return app_config_settings
    else:
        try:
            setting = AppConfig.query.filter_by(key=args).first().value
        except:
            setting = False
        return setting


def get_oms_settings(*args):
    if not args:
        try:
            oms_config_settings = {'Twilio Account SID': OmsConfig.query.filter_by(key='Twilio Account SID').first().value,
                                   'Twilio Auth Token': OmsConfig.query.filter_by(key='Twilio Auth Token').first().value,
                                   'Twilio Phone Number': OmsConfig.query.filter_by(key='Twilio Phone Number').first().value,
                                   'Call Response MP3': OmsConfig.query.filter_by(key='Call Response MP3').first().value,
                                   'Call Response MP3 Toggle': OmsConfig.query.filter_by(key='Call Response MP3 Toggle').first().value,
                                   'Call Response Text-to-Speech': OmsConfig.query.filter_by(key='Call Response Text-to-Speech').first().value,
                                   'Call Response Text-to-Speech Toggle': OmsConfig.query.filter_by(key='Call Response Text-to-Speech Toggle').first().value,
                                   'Phone Number Visibility': OmsConfig.query.filter_by(key='Phone Number Visibility').first().value}
        except:
            oms_config_settings = False
        return oms_config_settings
    else:
        setting = False
        # - Note: The HTML spec for setting a checkbox to checked/unchecked seems to be really shitty.
        # if args[0] == 'Phone Number Visibility':
        # if args[0] == 'Phone Number Visibility' or args[0] == 'Call Response MP3 Toggle' or args[0] == 'Call Response Text-to-Speech Toggle':
        if args == 'Phone Number Visibility' or args == 'Call Response MP3 Toggle' or args == 'Call Response Text-to-Speech Toggle':
            try:
                setting_inquiry = OmsConfig.query.filter_by(key=args).first().value
                if setting_inquiry.lower() == 'true':
                    setting = 'checked'
                elif setting_inquiry.lower() == 'false':
                    setting = ''
            except:
                setting = False
        else:
            try:
                setting = OmsConfig.query.filter_by(key=args).first().value
            except:
                setting = False
        return setting


def check_permissions_to_change_App_Naming_and_Aesthetics(current_user):
    return


def update_names_and_aesthetics(current_user, names_and_aesthetics_form):
    try:
        fields_to_update = 0
        form = names_and_aesthetics_form
        settings = ((form.app_name.data, AppConfig.query.filter_by(key='App Name')),
                    (form.app_icon.data, AppConfig.query.filter_by(key='App Icon')),
                    (form.app_title.data, AppConfig.query.filter_by(key='App Title')),
                    (form.app_short_title.data, AppConfig.query.filter_by(key='App Short-Title')),
                    (form.placeholders_toggle.data, AppConfig.query.filter_by(key='Toggle Placeholders')))

        for form_data, setting in settings:
            if  form_data != setting.first().value and form_data != '':
                fields_to_update += 1
                setting.update({'value': form_data})
                db.session.commit()

        if fields_to_update == 0:
            flash('No changes to user were detected in form submission. Data has been left unchanged.', 'info')
        else:
            flash('Settings successfully updated!', 'success')
    except:
        db.session.rollback()
        flash('Sorry! It seems an issue occurred while attempting to update settings. Please contact the application '
              'administrator.', 'warning')


def check_permissions_to_change_App_Secret_Key(current_user):
    return


def update_secret_key(current_user, secret_key_form):
    try:
        fields_to_update = 0
        form = secret_key_form
        settings = ((form.secret_key.data, AppConfig.query.filter_by(key='Secret Key')),)

        for form_data, setting in settings:
            # flash(form_data)
            # flash(setting.first().value)
            if form_data != setting.first().value and form_data != '':
                fields_to_update += 1
                setting.update({'value': form_data})
                db.session.commit()

        if fields_to_update == 0:
            flash('No changes to user were detected in form submission. Data has been left unchanged.', 'info')
        else:
            flash('Settings successfully updated!', 'success')
    except:
        db.session.rollback()
        flash('Sorry! It seems an issue occurred while attempting to update settings. Please contact the application '
              'administrator.', 'warning')


def check_permissions_to_change_App_Modules(current_user):
    return


def update_modules(current_user):
    return


def update_oms_settings(current_user, oms_settings_form):
    try:
        fields_to_update = 0
        form = oms_settings_form
        settings = ((form.twilio_account_sid.data, OmsConfig.query.filter_by(key='Twilio Account SID')),
                    (form.twilio_auth_token.data, OmsConfig.query.filter_by(key='Twilio Auth Token')),
                    (form.twilio_phone_number.data, OmsConfig.query.filter_by(key='Twilio Phone Number')),
                    (form.call_response_mp3.data, OmsConfig.query.filter_by(key='Call Response MP3')),
                    (form.call_response_text_to_speech.data, OmsConfig.query.filter_by(key='Call Response Text-to-Speech')),
                    (form.call_response_mp3_toggle.data, OmsConfig.query.filter_by(key='Call Response MP3 Toggle')),
                    (form.call_response_text_to_speech_toggle.data, OmsConfig.query.filter_by(key='Call Response Text-to-Speech Toggle')),
                    (form.phone_number_visibility.data, OmsConfig.query.filter_by(key='Phone Number Visibility')))

        for form_data, setting in settings:
            if form_data != setting.first().value and form_data != '':
                fields_to_update += 1
                setting.update({'value': form_data})
                db.session.commit()

        if fields_to_update == 0:
            flash('No changes to user were detected in form submission. Data has been left unchanged.', 'info')
        else:
            flash('Settings successfully updated!', 'success')
            flash('Now that you have updated these settings, the server will need to restart. Restart is currently not '
                  'automatic. Please have your server administrator restart the application server to fully apply these'
                  'changes.', 'info')
    except:
        db.session.rollback()
        flash('Sorry! It seems an issue occurred while attempting to update settings. Please contact the application '
              'administrator.', 'warning')

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


def update_self(update_form):
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

        if len(fields_to_update) == 0:
            flash('No changes to user were detected in form submission. User has been left unchanged.', 'info')
        else:
            user.update(dict(fields_to_update))
            db.session.commit()
            flash('User successfully updated!', 'success')
    except:
        db.session.rollback()
        flash('Sorry! It seems an issue occurred while attempting to add/update user. It may be possible that you have '
              'attempted to change unique information (ie. username, e-mail) that already exists for another user. If '
              'this is not the case, please contact the application administrator.', 'warning')


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
            billing_address_city='',
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
            phone1=format_phone_number(add_form.phone1.data),
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

def get_upload_columns(data_model):
    upload_columns = {'reqruied': '', 'optional': ''}
    upload_columns_lists = {'required': [], 'optional': []}
    for column, metadata in data_model.db_columns.items():
        if metadata['required'] == True:
            upload_columns_lists['required'].append(column)
        else:
            upload_columns_lists['optional'].append(column)
    upload_columns['required'] = make_string_list(upload_columns_lists['required'])
    upload_columns['optional'] = make_string_list(upload_columns_lists['optional'])
    return upload_columns


##############
# - Variables
