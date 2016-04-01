# - This was from Flask Mega Tutorial
# from flask.ext.wtf import Form
# from wtforms import StringField, BooleanField
# from wtforms.validators import DataRequired

# class LoginForm(Form):
#     openid = StringField('openid', validators=[DataRequired()])
#     remember_me = BooleanField('remember_me', default=False)

# - This is from RealPython
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')])


class UserAddForm(Form):
    form_id = 'User-Add-Form'
    username = StringField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField(
        'Repeat password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    groups = StringField(
        'username',
        validators=[Length(max=500)])
    permissions = StringField(
        'username',
        validators=[Length(max=500)])


class UserUpdateForm(Form):
    form_id = 'User-Update-Form'
    username = StringField(
        'username',
        validators=[Length(min=3, max=25)])
    email = StringField(
        'email',
        validators=[Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        'password',
        validators=[Length(min=6, max=25)])
    confirm = PasswordField(
        'Repeat password',
        validators=[EqualTo('password', message='Passwords must match.')])
    groups = StringField(
        'username',
        validators=[Length(max=500)])
    permissions = StringField(
        'username',
        validators=[Length(max=500)])


class CustomerAddForm(Form):
    form_id = 'User-Add-Form'
    username = StringField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField(
        'Repeat password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    groups = StringField(
        'username',
        validators=[Length(max=500)])
    permissions = StringField(
        'username',
        validators=[Length(max=500)])


class CustomerUpdateForm(Form):
    form_id = 'User-Update-Form'
    username = StringField(
        'username',
        validators=[Length(min=3, max=25)])
    email = StringField(
        'email',
        validators=[Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        'password',
        validators=[Length(min=6, max=25)])
    confirm = PasswordField(
        'Repeat password',
        validators=[EqualTo('password', message='Passwords must match.')])
    groups = StringField(
        'username',
        validators=[Length(max=500)])
    permissions = StringField(
        'username',
        validators=[Length(max=500)])


class PersonnelAddForm(Form):
    form_id = 'User-Add-Form'
    username = StringField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField(
        'Repeat password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    groups = StringField(
        'username',
        validators=[Length(max=500)])
    permissions = StringField(
        'username',
        validators=[Length(max=500)])


class PersonnelUpdateForm(Form):
    form_id = 'User-Update-Form'
    username = StringField(
        'username',
        validators=[Length(min=3, max=25)])
    email = StringField(
        'email',
        validators=[Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        'password',
        validators=[Length(min=6, max=25)])
    confirm = PasswordField(
        'Repeat password',
        validators=[EqualTo('password', message='Passwords must match.')])
    groups = StringField(
        'username',
        validators=[Length(max=500)])
    permissions = StringField(
        'username',
        validators=[Length(max=500)])
