# - This was from Flask Mega Tutorial
# from flask.ext.wtf import Form
# from wtforms import StringField, BooleanField
# from wtforms.validators import DataRequired

# class LoginForm(Form):
#     openid = StringField('openid', validators=[DataRequired()])
#     remember_me = BooleanField('remember_me', default=False)

# - This is from RealPython
from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, BooleanField, HiddenField
# from wtforms import SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

##############
# - Super Classes
class BaseForm(Form):
    @classmethod
    def append_field(cls, name, field):
        setattr(cls, name, field)
        return cls
    # submit = SubmitField('Submit')


##############
# - App Core Forms
class LoginForm(Form):
    username = StringField('Username', render_kw={"placeholder": "Username/E-mail"}, validators=[DataRequired()])
    password = PasswordField('Password', render_kw={"placeholder": "Password"}, validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False, id="remember_me")


class RegisterForm(Form):
    username = StringField('username', render_kw={"placeholder": "Username"},
                        validators=[DataRequired(), Length(min=6, max=25)])
    email = StringField('email', render_kw={"placeholder": "E-mail"},
                        validators=[DataRequired(), Email(message=None), Length(min=6, max=50)])
    password = PasswordField('password', render_kw={"placeholder": "Password"},
                        validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField('confirm password', render_kw={"placeholder": "Confirm Password..."},
                        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])


class Config_Names_and_Aesthetics(BaseForm):
    form_id = 'Config_Name-and-Aesthetics-Form'
    header = 'Application Naming & Aesthetics'
    crud_type = "Update"
    module = "App Administration"
    sub_module = "App Config"

    app_name = StringField('app_name', render_kw={"placeholder": "App Name", 'label': 'App Name'},
                       validators=[DataRequired(), Length(min=1, max=50)])
    app_icon = StringField('app_icon', render_kw={"placeholder": "App Icon", 'label': 'App Icon'},
                           validators=[DataRequired(), Length(min=1, max=100)])
    app_title = StringField('app_title', render_kw={"placeholder": "App Title", 'label': 'App Title'},
                           validators=[DataRequired(), Length(min=1, max=50)])
    app_short_title = StringField('app_short_title', render_kw={"placeholder": "App Shortened Title", 'label': 'App Shortened Title'},
                           validators=[DataRequired(), Length(min=1, max=50)])


class Config_Secret_Key(BaseForm):
    form_id = 'Config_Secret-Key-Form'
    header = 'Sessions Secret Key'
    crud_type = "Update"
    module = "App Administration"
    sub_module = "App Config"

    secret_key = StringField('secret_key', render_kw={"placeholder": "Secret Key", 'label': 'Secret Key'},
                           validators=[DataRequired(), Length(min=1, max=200)])


class Config_Modules(BaseForm):
    form_id = 'Config_Modules-Form'
    header = 'Module Management'
    crud_type = "Update"
    module = "App Administration"
    sub_module = "App Config"

    oms = BooleanField('oms', default=True, id="oms", render_kw={'label': 'Operations Management System'})
    crm = BooleanField('crm', default=True, id="crm", render_kw={'label': 'Customer Relationsip Management System'})
    hrm = BooleanField('hrm', default=True, id="hrm", render_kw={'label': 'Human Resources Management System'})
    ams = BooleanField('ams', default=True, id="ams", render_kw={'label': 'Accounting Management System'})
    mms = BooleanField('mms', default=True, id="mms", render_kw={'label': 'Marketing Management System'})


class UserAddForm(BaseForm):
    form_id = 'User-Add-Form'
    crud_type = "Add"
    module = "App Administration"
    sub_module = "User Management"

    username = StringField('username', render_kw={"placeholder": "Username", "section": "account", 'label': 'Username'},
        validators=[DataRequired(), Length(min=6, max=25)])
    email = StringField('email', render_kw={"placeholder": "E-mail", "section": "account", 'label': 'E-mail'},
        validators=[DataRequired(), Email(message=None), Length(min=6, max=50)])
    password = PasswordField('password', render_kw={"placeholder": "Password", "section": "account", 'label': 'Password'},
        validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField('confirm password', render_kw={"placeholder": "Confirm Password", "section": "account", 'label': 'Confirm Password'},
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    admin_role = SelectField('admin role', render_kw={"placeholder": "User/App Administration", "section": "admin", "icon": "fa fa-cogs"},
        choices=[('super', 'Super Admin'), ('basic', 'Basic Admin'), ('None', 'Normal User')])

    # - Need to fix this so that this isn't even needed. Unfortunately WTForms doesn't support dynamic field addition.
    # The code to dynamically add fields is in the 'BaseForm' class, and in the route in routes.py.
    oms_role = SelectField('oms role',
                           render_kw={"placeholder": "Operations Management", "section": "groups", "field_name": "Operations", "icon": "fa fa-fort-awesome"}, description="Operations",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])
    crm_role = SelectField('crm role',
                           render_kw={"placeholder": "Customer Relations", "section": "groups", "field_name": "Customer Relations", "icon": "ion-person-stalker"}, description="Customer Relations",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])
    hrm_role = SelectField('hrm role',
                           render_kw={"placeholder": "Human Resources", "section": "groups", "field_name": "Human Resources", "icon": "fa fa-users"}, description="Human Resources",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])
    ams_role = SelectField('ams role',
                           render_kw={"placeholder": "Accounting Management", "section": "groups", "field_name": "Accounting", "icon": "fa fa-bar-chart"}, description="Accounting",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])
    mms_role = SelectField('mms role',
                           render_kw={"placeholder": "Marketing Management", "section": "groups", "field_name": "Marketing", "icon": "fa fa-line-chart"}, description="Marketing",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])


class UserUpdateForm(BaseForm):
    form_id = 'User-Update-Form'
    crud_type = "Update"
    module = "App Administration"
    sub_module = "User Management"
    role_default = "null"

    user_id = HiddenField('user_id', validators=[Length(min=1, max=12)])
    username = StringField('username', render_kw={"placeholder": "Username", "section": "account", 'label': 'Username'},
                            validators=[Length(min=6, max=25)])
    email = StringField('email', render_kw={"placeholder": "E-mail", "section": "account", 'label': 'E-mail'},
                            validators=[Email(message=None), Length(min=6, max=50)])
    password = PasswordField('password', render_kw={"placeholder": "Leave blank to leave unchanged.", "section": "account", 'label': 'Password'},
                            validators=[Optional(), Length(min=6, max=25)])
    confirm = PasswordField('confirm password', render_kw={"placeholder": "Leave blank to leave unchanged.", "section": "account", 'label': 'Confirm Password'},
                            validators=[Optional(), EqualTo('password', message='Passwords must match.')])
    admin_role = SelectField('admin role', render_kw={"placeholder": "User/App Administration", "section": "admin", "icon": "fa fa-cogs"},
                             choices=[('null', ''), ('super', 'Super Admin'), ('basic', 'Basic Admin'), ('None', 'Normal User')], default=role_default)

    # - Need to fix this so that this isn't even needed. Unfortunately WTForms doesn't support dynamic field addition.
    # The code to dynamically add fields is in the 'BaseForm' class, and in the route in routes.py.
    oms_role = SelectField('oms role', render_kw={"placeholder": "Operations Management", "section": "groups", "field_name": "Operations", "icon": "fa fa-fort-awesome"}, description="Operations",
                           choices=[('null', ''), ('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')], default=role_default)
    crm_role = SelectField('crm role', render_kw={"placeholder": "Customer Relations", "section": "groups", "field_name": "Customer Relations", "icon": "ion-person-stalker"}, description="Customer Relations",
                           choices=[('null', ''), ('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')], default=role_default)
    hrm_role = SelectField('hrm role', render_kw={"placeholder": "Human Resources", "section": "groups", "field_name": "Human Resources", "icon": "fa fa-users"}, description="Human Resources",
                           choices=[('null', ''), ('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')], default=role_default)
    ams_role = SelectField('ams role', render_kw={"placeholder": "Accounting Management", "section": "groups", "field_name": "Accounting", "icon": "fa fa-bar-chart"}, description="Accounting",
                           choices=[('null', ''), ('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')], default=role_default)
    mms_role = SelectField('mms role', render_kw={"placeholder": "Marketing Management", "section": "groups", "field_name": "Marketing", "icon": "fa fa-line-chart"}, description="Marketing",
                           choices=[('null', ''), ('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')], default=role_default)


class UserDeleteForm(BaseForm):
    form_id = 'User-Delete-Form'
    crud_type = "Delete"
    module = "App Administration"
    sub_module = "User Management"

    user_id = HiddenField('user_id', validators=[Length(min=1, max=12)])


##############
# - CRM Forms
class CustomerAddForm(Form):
    form_id = 'Customer-Add-Form'
    crud_type = "Add"
    module = "Customer Relations"
    sub_module = "Customer List"

    first_name = StringField('first name', render_kw={"placeholder": "First Name", "section": "contact_info", 'label': 'First Name'},
                             validators=[DataRequired(), Length(min=3, max=25)])
    last_name = StringField('last name', render_kw={"placeholder": "Last Name", "section": "contact_info", 'label': 'Last Name'},
                            validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('email', render_kw={"placeholder": "E-mail", "section": "contact_info", 'label': 'E-mail'},
                        validators=[Email(message=None), Length(min=6, max=40)])
    phone_number = StringField('phone number', render_kw={"placeholder": "Phone Number", "section": "contact_info", 'label': 'Phone #'},
                               validators=[DataRequired(), Length(min=6, max=40)])


class CustomerUpdateForm(Form):
    form_id = 'Customer-Update-Form'
    crud_type = "Update"
    module = "Customer Relations"
    sub_module = "Customer List"

    customer_id = HiddenField('customer_id', validators=[Length(min=1, max=12)])
    first_name = StringField('first_name', render_kw={"placeholder": "First Name", "section": "contact_info", 'label': 'First Name'},
                             validators=[Length(min=3, max=25)])
    last_name = StringField('last_name', render_kw={"placeholder": "Last Name", "section": "contact_info", 'label': 'Last Name'},
                            validators=[Length(min=3, max=25)])
    email = StringField('email', render_kw={"placeholder": "E-mail", "section": "contact_info", 'label': 'E-mail'},
                        validators=[Email(message=None), Length(min=6, max=40)])
    phone_number = StringField('phone_number', render_kw={"placeholder": "Phone Number", "section": "contact_info", 'label': 'Phone #'},
                               validators=[Length(min=6, max=40)])

class CustomerDeleteForm(BaseForm):
    form_id = 'Customer-Delete-Form'
    crud_type = "Delete"
    module = "Customer Relations"
    sub_module = "Customer List"

    customer_id = HiddenField('customer_id', validators=[Length(min=1, max=12)])


##############
# - HRM Forms
class PersonnelAddForm(Form):
    form_id = 'Personnel-Add-Form'
    crud_type = "Add"
    module = "Human Resources"
    sub_module = "HR Management"

    first_name = StringField('first_name', render_kw={"placeholder": "First Name", "section": "contact_info", 'label': 'First Name'},
                             validators=[DataRequired(), Length(min=3, max=25)])
    last_name = StringField('last_name', render_kw={"placeholder": "Last Name", "section": "contact_info", 'label': 'Last Name'},
                            validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('email', render_kw={"placeholder": "E-mail", "section": "contact_info", 'label': 'E-mail'},
                        validators=[Email(message=None), Length(min=6, max=40)])
    phone_number = StringField('phone_number', render_kw={"placeholder": "Phone Number", "section": "contact_info", 'label': 'Phone #'},
                               validators=[DataRequired(), Length(min=6, max=40)])


class PersonnelUpdateForm(Form):
    form_id = 'Personnel-Update-Form'
    crud_type = "Update"
    module = "Human Resources"
    sub_module = "Personnel List"

    personnel_id = HiddenField('personnel_id', validators=[Length(min=1, max=12)])
    first_name = StringField('first_name', render_kw={"placeholder": "First Name", "section": "contact_info", 'label': 'First Name'},
                             validators=[Length(min=3, max=25)])
    last_name = StringField('last_name', render_kw={"placeholder": "Last Name", "section": "contact_info", 'label': 'Last Name'},
                            validators=[Length(min=3, max=25)])
    email = StringField('email', render_kw={"placeholder": "E-mail", "section": "contact_info", 'label': 'E-mail'},
                        validators=[Email(message=None), Length(min=6, max=40)])
    phone_number = StringField('phone_number', render_kw={"placeholder": "Phone Number", "section": "contact_info", 'label': 'Phone #'},
                               validators=[Length(min=6, max=40)])


class PersonelDeleteForm(BaseForm):
    form_id = 'Personnel-Delete-Form'
    crud_type = "Delete"
    module = "Human Resources"
    sub_module = "Personnel List"

    personnel_id = HiddenField('personnel_id', validators=[Length(min=1, max=12)])
