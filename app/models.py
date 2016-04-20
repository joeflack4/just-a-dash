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
    db_columns = [
        {'name': 'username', 'required': True},
        {'name': 'email', 'required': True},
        {'name': 'password', 'required': True},
        {'name': 'admin_role', 'required': False},
        {'name': 'oms_role', 'required': False},
        {'name': 'crm_role', 'required': False},
        {'name': 'hrm_role', 'required': False},
        {'name': 'ams_role', 'required': False},
        {'name': 'mms_role', 'required': False},
    ]

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
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
        user_rank = int

        def determine_rank(role_value):
            # unrecognized_role_values = []
            rank = int
            if role_value == 'master':
                rank = 0
            elif role_value == 'super':
                rank = 1
            elif role_value == 'basic':
                rank = 2
            elif role_value == 'None':
                rank = 3
            elif role_value == 'none':
                rank = 3
            elif role_value == '':
                rank = 3
            elif role_value == False:
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

        user_to_compare_rank = determine_rank(role_value)

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
    address_suite = db.Column(db.String(20))
    address_state = db.Column(db.String(2))
    address_county = db.Column(db.String(20))
    address_zip = db.Column(db.String(5))
    address_zip_extension = db.Column(db.String(4))
    relation_1_name = db.Column(db.String(100))
    relation_1_notes = db.Column(db.String(100))
    relation_2_name = db.Column(db.String(100))
    relation_2_notes = db.Column(db.String(100))
    notes_other = db.Column(db.String(100))

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
    db_columns = [
        {'name': 'name_last', 'required': True},
        {'name': 'name_first', 'required': True},
        {'name': 'name_prefix', 'required': False},
        {'name': 'name_suffix', 'required': False},
        {'name': 'name_middle', 'required': False},
        {'name': 'email1', 'required': False},
        {'name': 'email2', 'required': False},
        {'name': 'phone1', 'required': False},
        {'name': 'phone2', 'required': False},
        {'name': 'phone3', 'required': False},
        {'name': 'phone4', 'required': False},
        {'name': 'phone5', 'required': False},
        {'name': 'pii_dob', 'required': False},
        {'name': 'pii_other', 'required': False},
        {'name': 'phi', 'required': False},
        {'name': 'pfi', 'required': False},
        {'name': 'address_street', 'required': False},
        {'name': 'address_suite', 'required': False},
        {'name': 'address_state', 'required': False},
        {'name': 'address_county', 'required': False},
        {'name': 'address_zip', 'required': False},
        {'name': 'address_zip_extension', 'required': False},
        {'name': 'billing_method', 'required': False},
        {'name': 'billing_frequency', 'required': False},
        {'name': 'billing_relation_name', 'required': False},
        {'name': 'billing_email', 'required': False},
        {'name': 'billing_address_street', 'required': False},
        {'name': 'billing_address_suite', 'required': False},
        {'name': 'billing_address_state', 'required': False},
        {'name': 'billing_address_county', 'required': False},
        {'name': 'billing_address_zip', 'required': False},
        {'name': 'billing_address_zip_extension', 'required': False},
        {'name': 'billing_notes', 'required': False},
        {'name': 'relation_1_name', 'required': False},
        {'name': 'relation_1_role', 'required': False},
        {'name': 'relation_2_name', 'required': False},
        {'name': 'relation_2_role', 'required': False},
        {'name': 'relation_3_name', 'required': False},
        {'name': 'relation_3_role', 'required': False},
        {'name': 'relation_4_name', 'required': False},
        {'name': 'relation_4_role', 'required': False},
        {'name': 'relation_5_name', 'required': False},
        {'name': 'relation_5_role', 'required': False},
        {'name': 'customer_type', 'required': False},
        {'name': 'customer_type_id1', 'required': False},
        {'name': 'customer_type_id2', 'required': False},
        {'name': 'customer_type_id3', 'required': False},
        {'name': 'service_1_id', 'required': False},
        {'name': 'service_1_day', 'required': False},
        {'name': 'service_1_hours', 'required': False},
        {'name': 'service_1_type', 'required': False},
        {'name': 'service_1_rate', 'required': False},
        {'name': 'service_2_id', 'required': False},
        {'name': 'service_2_day', 'required': False},
        {'name': 'service_2_hours', 'required': False},
        {'name': 'service_2_type', 'required': False},
        {'name': 'service_2_rate', 'required': False},
        {'name': 'service_3_id', 'required': False},
        {'name': 'service_3_day', 'required': False},
        {'name': 'service_3_hours', 'required': False},
        {'name': 'service_3_type', 'required': False},
        {'name': 'service_3_rate', 'required': False},
        {'name': 'service_4_id', 'required': False},
        {'name': 'service_4_day', 'required': False},
        {'name': 'service_4_hours', 'required': False},
        {'name': 'service_4_type', 'required': False},
        {'name': 'service_4_rate', 'required': False},
        {'name': 'service_5_id', 'required': False},
        {'name': 'service_5_day', 'required': False},
        {'name': 'service_5_hours', 'required': False},
        {'name': 'service_5_type', 'required': False},
        {'name': 'service_5_rate', 'required': False},
        {'name': 'service_6_id', 'required': False},
        {'name': 'service_6_day', 'required': False},
        {'name': 'service_6_hours', 'required': False},
        {'name': 'service_6_type', 'required': False},
        {'name': 'service_6_rate', 'required': False},
        {'name': 'notes_case', 'required': False},
        {'name': 'notes_other', 'required': False},
    ]

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
    address_suite = db.Column(db.String(20))
    address_state = db.Column(db.String(2))
    address_county = db.Column(db.String(20))
    address_zip = db.Column(db.String(5))
    address_zip_extension = db.Column(db.String(4))
    billing_method = db.Column(db.String(50))
    billing_frequency = db.Column(db.String(50))
    billing_relation_name = db.Column(db.String(50))
    billing_email = db.Column(db.String(50))
    billing_address_street = db.Column(db.String(50))
    billing_address_suite = db.Column(db.String(20))
    billing_address_state = db.Column(db.String(2))
    billing_address_county = db.Column(db.String(20))
    billing_address_zip = db.Column(db.String(5))
    billing_address_zip_extension = db.Column(db.String(4))
    billing_notes = db.Column(db.String(50))
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
    notes_case = db.Column(db.String(100))
    notes_other = db.Column(db.String(100))

    def __init__(self, name_last, name_first):
        self.last_name = name_last
        self.first_name = name_first

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
    db_columns = [
        {'name': 'name_last', 'required': True},
        {'name': 'name_first', 'required': True},
        {'name': 'name_prefix', 'required': False},
        {'name': 'name_suffix', 'required': False},
        {'name': 'name_middle', 'required': False},
        {'name': 'email1', 'required': False},
        {'name': 'email2', 'required': False},
        {'name': 'phone1', 'required': False},
        {'name': 'phone2', 'required': False},
        {'name': 'phone3', 'required': False},
        {'name': 'phone4', 'required': False},
        {'name': 'phone5', 'required': False},
        {'name': 'pii_dob', 'required': False},
        {'name': 'pii_other', 'required': False},
        {'name': 'phi', 'required': False},
        {'name': 'pfi', 'required': False},
        {'name': 'address_street', 'required': False},
        {'name': 'address_suite', 'required': False},
        {'name': 'address_state', 'required': False},
        {'name': 'address_county', 'required': False},
        {'name': 'address_zip', 'required': False},
        {'name': 'address_zip_extension', 'required': False},
        {'name': 'relation_1_name', 'required': False},
        {'name': 'relation_1_notes', 'required': False},
        {'name': 'relation_2_name', 'required': False},
        {'name': 'relation_2_notes', 'required': False},
        {'name': 'notes_other', 'required': False},
    ]

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
    address_suite = db.Column(db.String(20))
    address_state = db.Column(db.String(2))
    address_county = db.Column(db.String(20))
    address_zip = db.Column(db.String(5))
    address_zip_extension = db.Column(db.String(4))
    relation_1_name = db.Column(db.String(100))
    relation_1_notes = db.Column(db.String(100))
    relation_2_name = db.Column(db.String(100))
    relation_2_notes = db.Column(db.String(100))
    notes_other = db.Column(db.String(100))

    def __init__(self, name_last):
        self.name_last = name_last

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
