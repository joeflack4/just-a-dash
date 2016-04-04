# - This was from Flask Mega Tutorial
# from flask.ext.wtf import Form
# from wtforms import StringField, BooleanField
# from wtforms.validators import DataRequired

# class LoginForm(Form):
#     openid = StringField('openid', validators=[DataRequired()])
#     remember_me = BooleanField('remember_me', default=False)

# - This is from RealPython
from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, BooleanField
# from wtforms import SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class BaseForm(Form):
    @classmethod
    def append_field(cls, name, field):
        setattr(cls, name, field)
        return cls
    # submit = SubmitField('Submit')


class LoginForm(Form):
    username = StringField('Username', render_kw={"placeholder": "Username/E-mail"},
                           validators=[DataRequired()])
    password = PasswordField('Password', render_kw={"placeholder": "Password"},
                             validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False, id="remember_me")


class RegisterForm(Form):
    username = StringField('username', render_kw={"placeholder": "Username"},
                           validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('email', render_kw={"placeholder": "E-mail"},
                        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField('password', render_kw={"placeholder": "Password"},
                             validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField('confirm password', render_kw={"placeholder": "Confirm Password..."},
                            validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])


class UserAddForm(BaseForm):
    form_id = 'User-Add-Form'
    action = "url_for('user_management')"

    username = StringField('username', render_kw={"placeholder": "Username", "section": "account"},
        validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('email', render_kw={"placeholder": "E-mail", "section": "account"},
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField('password', render_kw={"placeholder": "Password", "section": "account"},
        validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField('confirm password', render_kw={"placeholder": "Confirm Password", "section": "account"},
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    admin_role = SelectField('admin role', render_kw={"placeholder": "User/App Administration", "section": "admin"},
        choices=[('super', 'Super Admin'), ('basic', 'Basic Admin')])

    # - Need to fix this so that this isn't even needed. Unfortunately WTForms doesn't support dynamic field addition.
    # The code to dynamically add fields is in the 'BaseForm' class, and in the route in routes.py.
    oms_role = SelectField('oms role',
                           render_kw={"placeholder": "Operations Management", "section": "groups", "field_name": "Operations"}, description="Operations",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])
    crm_role = SelectField('crm role',
                           render_kw={"placeholder": "Customer Relations", "section": "groups", "field_name": "Customer Relations"}, description="Customer Relations",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])
    hrm_role = SelectField('hrm role',
                           render_kw={"placeholder": "Human Resources", "section": "groups", "field_name": "Human Resources"}, description="Human Resources",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])
    ams_role = SelectField('ams role',
                           render_kw={"placeholder": "Accounting Management", "section": "groups", "field_name": "Accounting"}, description="Accounting",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])
    mms_role = SelectField('mms role',
                           render_kw={"placeholder": "Marketing Management", "section": "groups", "field_name": "Marketing"}, description="Marketing",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])


class UserUpdateForm(BaseForm):
    form_id = 'User-Update-Form'
    crud_type = "Update"

    username = StringField('username', render_kw={"placeholder": "Username", "section": "account"},
                            validators=[Length(min=3, max=25)])
    email = StringField('email', render_kw={"placeholder": "E-mail", "section": "account"},
                            validators=[Email(message=None), Length(min=6, max=40)])
    password = PasswordField('password', render_kw={"placeholder": "Password", "section": "account"},
                            validators=[Length(min=6, max=25)])
    confirm = PasswordField('confirm password', render_kw={"placeholder": "Confirm Password", "section": "account"},
                            validators=[EqualTo('password', message='Passwords must match.')])
    admin_role = SelectField('admin role', render_kw={"placeholder": "User/App Administration", "section": "admin"},
                            choices=[('super', 'Super Admin'), ('basic', 'Basic Admin')])

    # - Need to fix this so that this isn't even needed. Unfortunately WTForms doesn't support dynamic field addition.
    # The code to dynamically add fields is in the 'BaseForm' class, and in the route in routes.py.
    oms_role = SelectField('oms role', render_kw={"placeholder": "Operations Management", "section": "groups", "field_name": "Operations"}, description="Operations",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])
    crm_role = SelectField('crm role', render_kw={"placeholder": "Customer Relations", "section": "groups", "field_name": "Customer Relations"}, description="Customer Relations",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])
    hrm_role = SelectField('hrm role', render_kw={"placeholder": "Human Resources", "section": "groups", "field_name": "Human Resources"}, description="Human Resources",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])
    ams_role = SelectField('ams role', render_kw={"placeholder": "Accounting Management", "section": "groups", "field_name": "Accounting"}, description="Accounting",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])
    mms_role = SelectField('mms role', render_kw={"placeholder": "Marketing Management", "section": "groups", "field_name": "Marketing"}, description="Marketing",
                           choices=[('None', 'Not a Member'), ('basic', 'Basic Group Admin'), ('super', 'Super Group Admin')])


class CustomerAddForm(Form):
    form_id = 'Customer-Add-Form'
    first_name = StringField('first name', render_kw={"placeholder": "first name"},
                             validators=[DataRequired(), Length(min=3, max=25)])
    last_name = StringField('last name', render_kw={"placeholder": "last name"},
                            validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('email', render_kw={"placeholder": "e-mail"},
                        validators=[Email(message=None), Length(min=6, max=40)])
    phone_number = StringField('phone number', render_kw={"placeholder": "phone number"},
                               validators=[DataRequired(), Length(min=6, max=40)])


class CustomerUpdateForm(Form):
    form_id = 'Customer-Update-Form'
    first_name = StringField('first_name', render_kw={"placeholder": "first name"},
                             validators=[Length(min=3, max=25)])
    last_name = StringField('last_name', render_kw={"placeholder": "last name"},
                            validators=[Length(min=3, max=25)])
    email = StringField('email', render_kw={"placeholder": "e-mail"},
                        validators=[Email(message=None), Length(min=6, max=40)])
    phone_number = StringField('phone_number', render_kw={"placeholder": "phone number"},
                               validators=[Length(min=6, max=40)])


class PersonnelAddForm(Form):
    form_id = 'Personnel-Add-Form'
    first_name = StringField('first_name', render_kw={"placeholder": "first name"},
                             validators=[DataRequired(), Length(min=3, max=25)])
    last_name = StringField('last_name', render_kw={"placeholder": "last name"},
                            validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('email', render_kw={"placeholder": "e-mail"},
                        validators=[Email(message=None), Length(min=6, max=40)])
    phone_number = StringField('phone_number', render_kw={"placeholder": "phone number"},
                               validators=[DataRequired(), Length(min=6, max=40)])


class PersonnelUpdateForm(Form):
    form_id = 'Personnel-Update-Form'
    first_name = StringField('first_name', render_kw={"placeholder": "first name"},
                             validators=[Length(min=3, max=25)])
    last_name = StringField('last_name', render_kw={"placeholder": "last name"},
                            validators=[Length(min=3, max=25)])
    email = StringField('email', render_kw={"placeholder": "e-mail"},
                        validators=[Email(message=None), Length(min=6, max=40)])
    phone_number = StringField('phone_number', render_kw={"placeholder": "phone number"},
                               validators=[Length(min=6, max=40)])
