"""Operations"""


############
# - Modules - OMS
@app.route('/oms-home')
@login_required
@oms_basic_admin_required
def oms_home():
    logged_in = current_user.is_authenticated
    login_form = LoginForm(request.form)

    return render_template('modules/operations/home.html',
                           icon="fa fa-dashboard",
                           module_abbreviation="OMS",
                           module_name="Operations Management",
                           page_name="OMS Home",
                           app_config_settings=get_app_settings(),
                           messages=db.session.query(Messages),
                           notifications=db.session.query(AppNotifications),
                           profile_form=UserUpdateForm(request.form),
                           login_form=login_form,
                           current_user=current_user,
                           logged_in=logged_in)


@app.route('/operations')
@login_required
@oms_basic_admin_required
def operations(*args):
    logged_in = current_user.is_authenticated
    login_form = LoginForm(request.form)
    render_settings = {'Phone Number Visibility': OmsConfig.query.filter_by(key='Phone Number Visibility').first().value.lower(),
                       'Twilio Phone Number': OmsConfig.query.filter_by(key='Twilio Phone Number').first().value}

    try:
        check_in_type = args[0]
    except:
        check_in_type = None

    try:
        # Determine what kind of check-in is being executed.
        if check_in_type == "sms_check_in":
            check_in_entries = sms_check_in_data()
        elif check_in_type == "call_check_in":
            check_in_entries = call_check_in_data()
        elif check_in_type == None:
            check_in_entries = call_check_in_data()
        else:
            check_in_entries = {".": {"timestamp": ".", "first_name": ".", "last_name": ".", "phone_number": "."}}

        # Check for errors.
        critical_settings = ('Twilio Phone Number', 'Twilio Auth Token', 'Twilio Account SID')
        critical_settings_errors = []
        for setting in critical_settings:
            if OmsConfig.query.filter_by(key=setting).first().value == '':
                critical_settings_errors.append(setting)
            elif not OmsConfig.query.filter_by(key=setting).first().value:
                critical_settings_errors.append(setting)
        if critical_settings_errors != []:
            error_message = Markup('One or more errors occurred related to check-in submodule settings. The following '
                                   'setting(s) have not yet been configured, and may cause this submodule to behave '
                                   'incorrectly: {}'.format(make_string_list(critical_settings_errors)) +
                                   '. Please have the master user update module settings, then have the server '
                                   'administrator reset the server to apply settings.')
            flash(error_message, 'danger')

        return render_template('modules/operations/index.html',
                               icon="fa fa-fort-awesome",
                               module_abbreviation="OMS",
                               module_name="Operations Management",
                               page_name="OMS Home",
                               app_config_settings=get_app_settings(),
                               check_in_entries=check_in_entries,
                               messages=db.session.query(Messages),
                               notifications=db.session.query(AppNotifications),
                               login_form=login_form,
                               current_user=current_user,
                               logged_in=logged_in,
                               render_settings=render_settings)
    except:
        flash('Attempted to load check-in submodule, but an error occurred. Module settings may not be configured '
              'correctly. Please have the master user update module settings, then have the server administrator reset '
              'the server to apply settings.', 'danger')
        return redirect(url_for('root_path'))