from flask import flash, Markup
from app import db
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


db.Base = declarative_base()

# - To Do: Figure out relational mapping.
# user_messages = db.Table('user_messages', db.Base.metadata,
#     db.Column('user_id', db.Integer, ForeignKey('user.id')),
#     db.Column('messages_id', db.Integer, ForeignKey('messages.id'))
# )


##############
# - Super Classes
class Base_Model(db.Model):
    __abstract__ = True

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


class Base_Config(Base_Model):
    __abstract__ = True

    key = db.Column(db.String(100), primary_key=True, nullable=False)
    value = db.Column(db.String(200), nullable=False)
    permission_level = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def __init__(self, key, value, permission_level, active):
        self.key = key
        self.value = value
        self.permission_level = permission_level
        self.active = active

    def __repr__(self):
        return '<key name: {}>'.format(self.key)


##############
# - App Core Models
class Config(Base_Config):
    __tablename__ = 'app_config'


class Modules(Base_Model):
    __tablename__ = 'app_module-registry'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    abbreviation = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, abbreviation, description, active):
        self.name = name
        self.abbreviation = abbreviation
        self.description = description
        self.active = active

    def __repr__(self):
        return '<module name: {}>'.format(self.id)


class User(Base_Model):
    __tablename__ = 'app_users'
    # - db_columns is used for validating .csv imports.
    role_selectors = ('super', 'basic', 'none', '')

    db_columns = {
        'username': {'required': True, 'validators': 'string', 'validator_parameters': {'min': 6, 'max': 25}},
        'email': {'required': True, 'validators': 'email', 'validator_parameters': {'min': 6, 'max': 25}},
        'password': {'required': True, 'validators': 'string', 'validator_parameters': {'min': 6, 'max': 25}},
        'admin_role': {'required': False, 'validators': 'selection', 'validator_parameters': role_selectors},
        'oms_role': {'required': False, 'validators': 'selection', 'validator_parameters': role_selectors},
        'crm_role': {'required': False, 'validators': 'selection', 'validator_parameters': role_selectors},
        'hrm_role': {'required': False, 'validators': 'selection', 'validator_parameters': role_selectors},
        'ams_role': {'required': False, 'validators': 'selection', 'validator_parameters': role_selectors},
        'mms_role': {'required': False, 'validators': 'selection', 'validator_parameters': role_selectors}
    }

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    admin_role = db.Column(db.String(20))
    oms_role = db.Column(db.String(20))
    crm_role = db.Column(db.String(20))
    hrm_role = db.Column(db.String(20))
    ams_role = db.Column(db.String(20))
    mms_role = db.Column(db.String(20))

    # - To Do: Figure out relational mapping.
    # http: // docs.sqlalchemy.org / en / latest / orm / basic_relationships.html  # many-to-many
    # sent_messages = relationship("Messages", backref="user")
    # received_messages = relationship("Messages", backref="user")
    # received_messages = relationship(
    #     "messages",
    #     secondary=user_messages,
    #     back_populates="user")

    def __init__(self, username, email, password, admin_role, oms_role, crm_role, hrm_role, ams_role, mms_role):
        self.username = username
        self.email = email
        # self.password = bcrypt.generate_password_hash(str(password).encode('utf-8'))
        # print(self.password)

        # - worked with db_create.py / but switched to werkzeug security
        # self.password = bcrypt.generate_password_hash(password)

        # self.password = bcrypt.generate_password_hash(str(password))
        # print(self.password)
        # self.password = password
        # print(self.password)

        self.set_password(password)
        self.admin_role = admin_role
        self.oms_role = oms_role
        self.crm_role = crm_role
        self.hrm_role = hrm_role
        self.ams_role = ams_role
        self.mms_role = mms_role

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        # Due to a weird pycharm bug, or perhaps dependency issue with python environment, it may sometimes falseley state that 'unicode' is not a valid reference.
        return self.id

    def check_administrative_superiority(self, role, role_value):
        role_val = role_value.lower()
        user_rank = int

        def determine_rank(role_val):
            # unrecognized_role_values = []
            rank = int
            if role_val == 'master':
                rank = 0
            elif role_val == 'super':
                rank = 1
            elif role_val == 'basic':
                rank = 2
            elif role_val == 'None':
                rank = 3
            elif role_val == 'none':
                rank = 3
            elif role_val == '':
                rank = 3
            elif role_val == False:
                rank = 3
            else:
                # Number below chosen randomly. Let's hope that 777+ ranks aren't necessary for any users. If so, this
                # will have to be re-factored.
                error_message = Markup('An error occurred while trying to assess user permissions. The following permission level was '
                      'not recognized: <strong>{}</strong>'.format(role_value) + '. Only the following permission levels are valid: '
                      '"master", "super, "basic", and "none". Please change value of permission level(s) and try again.')
                flash(error_message, 'danger')
                rank = 777
                # unrecognized_role_values.append(role_value)
            return rank

        if role == 'admin_role':
            user_rank = determine_rank(self.admin_role)
        elif role == 'oms_role':
            user_rank = determine_rank(self.oms_role)
        elif role == 'crm_role':
            user_rank = determine_rank(self.crm_role)
        elif role == 'hrm_role':
            user_rank = determine_rank(self.hrm_role)
        elif role == 'ams_role':
            user_rank = determine_rank(self.ams_role)
        elif role == 'mms_role':
            user_rank = determine_rank(self.mms_role)

        user_to_compare_rank = determine_rank(role_val)

        is_superior = bool
        if user_rank < user_to_compare_rank:
            is_superior = True
        elif user_to_compare_rank <= user_rank:
           is_superior = False
        return is_superior

    def check_administrative_authority(self, role, role_values_to_assign):
        authority = self.check_administrative_superiority(role, role_values_to_assign)
        return authority

    def __repr__(self):
        return '<user id: {}>'.format(self.id)


class Roles(Base_Model):
    __tablename__ = 'app_roles'
    # - admin role permissions
    # 	- role (pk)  /  permission name / r / w / u / d
    # - custom admin permissions
    # 	- id # / permission name  / r / w / u / d
    module_abbreviation = db.Column(db.String(3), primary_key=True)
    role = db.Column(db.String(20), primary_key=True)
    permission_level = db.Column(db.Integer, nullable=False)

    def __init__(self, module_abbreviation, role, permission_level):
        self.module_abbreviation = module_abbreviation
        self.role = role
        self.permission_level = permission_level

    def __repr__(self):
        return '<role/module: {}/{}>'.format(self.role, self.module_abbreviation)


class Permissions(Base_Model):
    __tablename__ = 'app_permissions'
    __table_args__ = tuple(UniqueConstraint("module", "role"))

    # - table (user id #  /  group name  /  read  /  write  /  update  / delete
    # - need a relationship here with roles

    # debugging -- this probably not needed below (id)
    # id = db.Column(db.Integer, primary_key=True)

    # role = db.Column(db.String(20), foreign_key=True)
    # module = db.Column(db.String(3), foreign_key=True)

    module = db.Column(db.String(3), primary_key=True)
    role = db.Column(db.String(20), primary_key=True)
    permission = db.Column(db.String(80), nullable=False)
    read = db.Column(db.Boolean, nullable=False)
    write = db.Column(db.Boolean, nullable=False)
    update = db.Column(db.Boolean, nullable=False)
    delete = db.Column(db.Boolean, nullable=False)

    def __init__(self, module, role, permission, r, w, u, d):
        self.module = module
        self.role = role
        self.permission = permission
        self.read = r
        self.write = w
        self.update = u
        self.delete = d

    def __repr__(self):
        return '<role/module permission: {}/{} {}>'.format(self.role, self.module, self.permission)


class Messages(Base_Model):
    __tablename__ = 'app_messages'

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    type = db.Column(db.String(20))
    # Type examples: UserMessages, Notifications, Tasks, etc.
    subcategory = db.Column(db.String(20))
    # Subcategory examples: News, updates, etc.
    title = db.Column(db.String(30))
    body = db.Column(db.String(1000))
    author = db.Column(db.String(30))
    delivery_methods = db.Column(db.String(200))
    # Delivery Method examples: To webapp, native app, push notification, SMS, e-mail, phone call, etc.
    notes = db.Column(db.String())
    # - To Do: Figure out relational mapping.
    # user_id = db.Column(db.Integer, ForeignKey('user.id'))
    # destinations = db.Column(db.String())
    # Destinations examples: To users, groups.
    # destinations = relationship(
    #     "user",
    #     secondary=user_messages,
    #     back_populates="messages")

    def __init__(self, message_type, subcategory, title, body, author, destinations, delivery_methods):
        self.datetime = datetime.now()
        self.type = message_type
        self.subcategory = subcategory
        self.title = title
        self.body = body
        self.author = author
        self.destinations = destinations
        self.delivery_methods = delivery_methods

    def __repr__(self):
        return '<message id: {}>'.format(self.id)


class AppNotifications(Base_Model):
    __tablename__ = 'app_notifications'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True)
    datetime = db.Column(db.DateTime)
    type = db.Column(db.String(20))
    subcategory = db.Column(db.String(20))
    body = db.Column(db.String(1000))
    author = db.Column(db.String(30))
    delivery_methods = db.Column(db.String(200))
    notes = db.Column(db.String())

    def __init__(self, message_type, subcategory, title, body, author, destinations, delivery_methods):
        self.datetime = datetime.now()
        self.type = message_type
        self.subcategory = subcategory
        self.title = title
        self.body = body
        self.author = author
        self.destinations = destinations
        self.delivery_methods = delivery_methods

    def __repr__(self):
        return '<message id: {}>'.format(self.id)


class Contacts(Base_Model):
    __tablename__ = 'app_contacts'

    id = db.Column(db.Integer, primary_key=True)
    name_last = db.Column(db.String(80), nullable=False)
    name_first = db.Column(db.String(80), nullable=False)
    name_prefix = db.Column(db.String(80))
    name_suffix = db.Column(db.String(80))
    name_middle = db.Column(db.String(80))
    email1 = db.Column(db.String(120))
    email2 = db.Column(db.String(120))
    phone1 = db.Column(db.String(20))
    phone2 = db.Column(db.String(20))
    phone3 = db.Column(db.String(20))
    phone4 = db.Column(db.String(20))
    phone5 = db.Column(db.String(20))
    pii_dob = db.Column(db.String(10))
    pii_other = db.Column(db.String(500))
    phi = db.Column(db.String(500))
    pfi = db.Column(db.String(500))
    address_street = db.Column(db.String(50))
    address_suite = db.Column(db.String(30))
    address_state = db.Column(db.String(2))
    address_county = db.Column(db.String(20))
    address_zip = db.Column(db.String(5))
    address_zip_extension = db.Column(db.String(4))
    relation_1_name = db.Column(db.String(100))
    relation_1_notes = db.Column(db.String(500))
    relation_2_name = db.Column(db.String(100))
    relation_2_notes = db.Column(db.String(500))
    notes_other = db.Column(db.String(1000))

    def __init__(self, name_last, name_first):
        self.last_name = name_last
        self.first_name = name_first

    def __repr__(self):
        return '<contact id: {}>'.format(self.id)


##############
# - CRM Models
class CRM_Config(Base_Config):
    __tablename__ = 'crm_config'


class Customers(Base_Model):
    __tablename__ = 'crm_customers'
    # - db_columns is used for validating .csv imports.
    db_columns = {
        'name_last': {'required': True, 'validators': 'string', 'validator_parameters': {'min': 1, 'max': 50}},
        'name_first': {'required': True, 'validators': 'string', 'validator_parameters': {'min': 1, 'max': 50}},
        'name_prefix': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'name_suffix': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'name_middle': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'email1': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'email2': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'phone1': {'required': True, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'phone2': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'phone3': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'phone4': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'phone5': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'pii_dob': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'pii_other': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'phi': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'pfi': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'address_street': {'required': True, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'address_suite': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 30}},
        'address_city': {'required': True, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'address_state': {'required': True, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'address_county': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'address_zip': {'required': True, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'address_zip_extension': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'billing_method': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'billing_frequency': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'billing_relation_name': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'billing_email': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'billing_address_street': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'billing_address_suite': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 30}},
        'billing_address_state': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'billing_address_county': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'billing_address_zip': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'billing_address_zip_extension': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'billing_notes': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 1000}},
        'relation_1_name': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'relation_1_role': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'relation_2_name': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'relation_2_role': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'relation_3_name': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'relation_3_role': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'relation_4_name': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'relation_4_role': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'relation_5_name': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'relation_5_role': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'customer_type': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'customer_type_id1': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'customer_type_id2': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'customer_type_id3': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_1_id': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_1_day': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_1_hours': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_1_type': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_1_rate': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_2_id': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_2_day': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_2_hours': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_2_type': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_2_rate': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_3_id': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_3_day': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_3_hours': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_3_type': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_3_rate': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_4_id': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_4_day': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_4_hours': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_4_type': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_4_rate': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_5_id': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_5_day': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_5_hours': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_5_type': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_5_rate': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_6_id': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_6_day': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_6_hours': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_6_type': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'service_6_rate': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
        'notes_case': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 1000}},
        'notes_other': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 1000}}
    }

    id = db.Column(db.Integer, primary_key=True)
    name_last = db.Column(db.String(80), nullable=False)
    name_first = db.Column(db.String(80), nullable=False)
    name_prefix = db.Column(db.String(80))
    name_suffix = db.Column(db.String(80))
    name_middle = db.Column(db.String(80))
    email1 = db.Column(db.String(120))
    email2 = db.Column(db.String(120))
    phone1 = db.Column(db.String(20))
    phone2 = db.Column(db.String(20))
    phone3 = db.Column(db.String(20))
    phone4 = db.Column(db.String(20))
    phone5 = db.Column(db.String(20))
    pii_dob = db.Column(db.String(10))
    pii_other = db.Column(db.String(500))
    phi = db.Column(db.String(500))
    pfi = db.Column(db.String(500))
    address_street = db.Column(db.String(50))
    address_suite = db.Column(db.String(30))
    address_city = db.Column(db.String(30))
    address_state = db.Column(db.String(2))
    address_county = db.Column(db.String(20))
    address_zip = db.Column(db.String(5))
    address_zip_extension = db.Column(db.String(4))
    billing_method = db.Column(db.String(50))
    billing_frequency = db.Column(db.String(50))
    billing_relation_name = db.Column(db.String(50))
    billing_email = db.Column(db.String(50))
    billing_address_street = db.Column(db.String(50))
    billing_address_suite = db.Column(db.String(30))
    billing_address_state = db.Column(db.String(2))
    billing_address_county = db.Column(db.String(20))
    billing_address_zip = db.Column(db.String(5))
    billing_address_zip_extension = db.Column(db.String(4))
    billing_notes = db.Column(db.String(1000))
    relation_1_name = db.Column(db.String(100))
    relation_1_role = db.Column(db.String(100))
    relation_2_name = db.Column(db.String(100))
    relation_2_role = db.Column(db.String(100))
    relation_3_name = db.Column(db.String(100))
    relation_3_role = db.Column(db.String(100))
    relation_4_name = db.Column(db.String(100))
    relation_4_role = db.Column(db.String(100))
    relation_5_name = db.Column(db.String(100))
    relation_5_role = db.Column(db.String(100))
    customer_type = db.Column(db.String(100))
    customer_type_id1 = db.Column(db.String(100))
    customer_type_id2 = db.Column(db.String(100))
    customer_type_id3 = db.Column(db.String(100))
    service_1_id = db.Column(db.String(100))
    service_1_day = db.Column(db.String(100))
    service_1_hours = db.Column(db.String(100))
    service_1_type = db.Column(db.String(100))
    service_1_rate = db.Column(db.String(10))
    service_2_id = db.Column(db.String(100))
    service_2_day = db.Column(db.String(100))
    service_2_hours = db.Column(db.String(100))
    service_2_type = db.Column(db.String(100))
    service_2_rate = db.Column(db.String(10))
    service_3_id = db.Column(db.String(100))
    service_3_day = db.Column(db.String(100))
    service_3_hours = db.Column(db.String(100))
    service_3_type = db.Column(db.String(100))
    service_3_rate = db.Column(db.String(10))
    service_4_id = db.Column(db.String(100))
    service_4_day = db.Column(db.String(100))
    service_4_hours = db.Column(db.String(100))
    service_4_type = db.Column(db.String(100))
    service_4_rate = db.Column(db.String(10))
    service_5_id = db.Column(db.String(100))
    service_5_day = db.Column(db.String(100))
    service_5_hours = db.Column(db.String(100))
    service_5_type = db.Column(db.String(100))
    service_5_rate = db.Column(db.String(10))
    service_6_id = db.Column(db.String(100))
    service_6_day = db.Column(db.String(100))
    service_6_hours = db.Column(db.String(100))
    service_6_type = db.Column(db.String(100))
    service_6_rate = db.Column(db.String(10))
    notes_case = db.Column(db.String(1000))
    notes_other = db.Column(db.String(1000))

    def __init__(self, name_last, name_first, name_prefix, name_suffix, name_middle, email1, email2, phone1, phone2,
                 phone3, phone4, phone5, pii_dob, pii_other, phi, pfi, address_street, address_suite, address_city,
                 address_state, address_county, address_zip, address_zip_extension, billing_method, billing_frequency,
                 billing_relation_name, billing_email, billing_address_street, billing_address_suite,
                 billing_address_state, billing_address_county, billing_address_zip, billing_address_zip_extension,
                 billing_notes, relation_1_name, relation_1_role, relation_2_name, relation_2_role, relation_3_name,
                 relation_3_role, relation_4_name, relation_4_role, relation_5_name, relation_5_role, customer_type,
                 customer_type_id1, customer_type_id2, customer_type_id3, service_1_id, service_1_day, service_1_hours,
                 service_1_type, service_1_rate, service_2_id, service_2_day, service_2_hours, service_2_type,
                 service_2_rate, service_3_id, service_3_day, service_3_hours, service_3_type, service_3_rate,
                 service_4_id, service_4_day, service_4_hours, service_4_type, service_4_rate, service_5_id,
                 service_5_day, service_5_hours, service_5_type, service_5_rate, service_6_id, service_6_day,
                 service_6_hours, service_6_type, service_6_rate, notes_case, notes_other):
        self.name_last = name_last
        self.name_first = name_first
        self.name_prefix = name_prefix
        self.name_suffix = name_suffix
        self.name_middle = name_middle
        self.email1 = email1
        self.email2 = email2
        self.phone1 = phone1
        self.phone2 = phone2
        self.phone3 = phone3
        self.phone4 = phone4
        self.phone5 = phone5
        self.pii_dob = pii_dob
        self.pii_other = pii_other
        self.phi = phi
        self.pfi = pfi
        self.address_street = address_street
        self.address_suite = address_suite
        self.address_city = address_city
        self.address_state = address_state
        self.address_county = address_county
        self.address_zip = address_zip
        self.address_zip_extension = address_zip_extension
        self.billing_method = billing_method
        self.billing_frequency = billing_frequency
        self.billing_relation_name = billing_relation_name
        self.billing_email = billing_email
        self.billing_address_street = billing_address_street
        self.billing_address_suite = billing_address_suite
        self.billing_address_state = billing_address_state
        self.billing_address_county = billing_address_county
        self.billing_address_zip = billing_address_zip
        self.billing_address_zip_extension = billing_address_zip_extension
        self.billing_notes = billing_notes
        self.relation_1_name = relation_1_name
        self.relation_1_role = relation_1_role
        self.relation_2_name = relation_2_name
        self.relation_2_role = relation_2_role
        self.relation_3_name = relation_3_name
        self.relation_3_role = relation_3_role
        self.relation_4_name = relation_4_name
        self.relation_4_role = relation_4_role
        self.relation_5_name = relation_5_name
        self.relation_5_role = relation_5_role
        self.customer_type = customer_type
        self.customer_type_id1 = customer_type_id1
        self.customer_type_id2 = customer_type_id2
        self.customer_type_id3 = customer_type_id3
        self.service_1_id = service_1_id
        self.service_1_day = service_1_day
        self.service_1_hours = service_1_hours
        self.service_1_type = service_1_type
        self.service_1_rate = service_1_rate
        self.service_2_id = service_2_id
        self.service_2_day = service_2_day
        self.service_2_hours = service_2_hours
        self.service_2_type = service_2_type
        self.service_2_rate = service_2_rate
        self.service_3_id = service_3_id
        self.service_3_day = service_3_day
        self.service_3_hours = service_3_hours
        self.service_3_type = service_3_type
        self.service_3_rate = service_3_rate
        self.service_4_id = service_4_id
        self.service_4_day = service_4_day
        self.service_4_hours = service_4_hours
        self.service_4_type = service_4_type
        self.service_4_rate = service_4_rate
        self.service_5_id = service_5_id
        self.service_5_day = service_5_day
        self.service_5_hours = service_5_hours
        self.service_5_type = service_5_type
        self.service_5_rate = service_5_rate
        self.service_6_id = service_6_id
        self.service_6_day = service_6_day
        self.service_6_hours = service_6_hours
        self.service_6_type = service_6_type
        self.service_6_rate = service_6_rate
        self.notes_case = notes_case
        self.notes_other = notes_other

def __repr__(self):
        return '<customer id: {}>'.format(self.id)


class Agencies(Base_Model):
    __tablename__ = 'crm_agencies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    abbreviation = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<agency name: {}>'.format(self.id)


##############
# - HRM Models
class HRM_Config(Base_Config):
    __tablename__ = 'hrm_config'


class Personnel(Base_Model):
    __tablename__ = 'hrm_personnel'
    # - db_columns is used for validating .csv imports.
    db_columns = {
         'name_last': {'required': True, 'validators': 'string', 'validator_parameters': {'min': 1, 'max': 50}},
         'name_first': {'required': True, 'validators': 'string', 'validator_parameters': {'min': 1, 'max': 50}},
         'name_prefix': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'name_suffix': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'name_middle': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'email1': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'email2': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'phone1': {'required': True, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'phone2': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'phone3': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'phone4': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'phone5': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'pii_dob': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'pii_other': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'phi': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'pfi': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'address_street': {'required': True, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'address_suite': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 30}},
         'address_city': {'required': True, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'address_state': {'required': True, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'address_county': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'address_zip': {'required': True, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'address_zip_extension': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'relation_1_name': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'relation_1_notes': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 500}},
         'relation_2_name': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 50}},
         'relation_2_notes': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 500}},
         'notes_other': {'required': False, 'validators': 'string', 'validator_parameters': {'max': 1000}}
    }

    id = db.Column(db.Integer, primary_key=True)
    name_last = db.Column(db.String(80), nullable=False)
    name_first = db.Column(db.String(80), nullable=False)
    name_prefix = db.Column(db.String(80))
    name_suffix = db.Column(db.String(80))
    name_middle = db.Column(db.String(80))
    email1 = db.Column(db.String(120))
    email2 = db.Column(db.String(120))
    phone1 = db.Column(db.String(20))
    phone2 = db.Column(db.String(20))
    phone3 = db.Column(db.String(20))
    phone4 = db.Column(db.String(20))
    phone5 = db.Column(db.String(20))
    pii_dob = db.Column(db.String(10))
    pii_other = db.Column(db.String(500))
    phi = db.Column(db.String(500))
    pfi = db.Column(db.String(500))
    address_street = db.Column(db.String(50))
    address_suite = db.Column(db.String(30))
    address_city = db.Column(db.String(30))
    address_state = db.Column(db.String(2))
    address_county = db.Column(db.String(20))
    address_zip = db.Column(db.String(5))
    address_zip_extension = db.Column(db.String(4))
    relation_1_name = db.Column(db.String(100))
    relation_1_notes = db.Column(db.String(500))
    relation_2_name = db.Column(db.String(100))
    relation_2_notes = db.Column(db.String(500))
    notes_other = db.Column(db.String(1000))

    def __init__(self, name_last, name_first, name_prefix, name_suffix, name_middle, email1, email2, phone1, phone2,
                 phone3, phone4, phone5, pii_dob, pii_other, phi, pfi, address_street, address_suite, address_city,
                 address_state, address_county, address_zip, address_zip_extension, relation_1_name, relation_1_notes,
                 relation_2_name, relation_2_notes, notes_other):
        self.name_last = name_last
        self.name_first = name_first
        self.name_prefix = name_prefix
        self.name_suffix = name_suffix
        self.name_middle = name_middle
        self.email1 = email1
        self.email2 = email2
        self.phone1 = phone1
        self.phone2 = phone2
        self.phone3 = phone3
        self.phone4 = phone4
        self.phone5 = phone5
        self.pii_dob = pii_dob
        self.pii_other = pii_other
        self.phi = phi
        self.pfi = pfi
        self.address_street = address_street
        self.address_suite = address_suite
        self.address_city = address_city
        self.address_state = address_state
        self.address_county = address_county
        self.address_zip = address_zip
        self.address_zip_extension = address_zip_extension
        self.relation_1_name = relation_1_name
        self.relation_1_notes = relation_1_notes
        self.relation_2_name = relation_2_name
        self.relation_2_notes = relation_2_notes
        self.notes_other = notes_other

    def __repr__(self):
        return '<personnel id: {}>'.format(self.id)


##############
# - Operations Management Models
class OMS_Config(Base_Config):
    __tablename__ = 'oms_config'


##############
# - Accounting Management Models
class AMS_Config(Base_Config):
    __tablename__ = 'ams_config'


##############
# - Marketing Models
class MMS_Config(Base_Config):
    __tablename__ = 'mms_config'

# - Linguistic analysis sub-module models.
class Result(Base_Model):
    __tablename__ = 'mms_word-analysis-results'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    url = db.Column(db.String(300))
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.datetime = datetime.now()
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<result id: {}>'.format(self.id)
