# - Imports
from flask import flash, Markup
from werkzeug.security import generate_password_hash
from app import db
# from requests import request
from .models import User
# from .forms import UserAddForm


# - Variables


# - Functions
# -- User Management
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

# - Classes
