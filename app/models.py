from app import db, bcrypt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

db.Base = declarative_base()

# - To Do: Figure out relational mapping.
# user_messages = db.Table('user_messages', db.Base.metadata,
#     db.Column('user_id', db.Integer, ForeignKey('user.id')),
#     db.Column('messages_id', db.Integer, ForeignKey('messages.id'))
# )


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    admin_role = db.Column(db.String(20))
    group_roles = db.Column(db.String(500))
    # - To Do: Figure out relational mapping.
    # http: // docs.sqlalchemy.org / en / latest / orm / basic_relationships.html  # many-to-many
    # sent_messages = relationship("Messages", backref="user")
    # received_messages = relationship("Messages", backref="user")
    # received_messages = relationship(
    #     "messages",
    #     secondary=user_messages,
    #     back_populates="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        # self.password = bcrypt.generate_password_hash(str(password).encode('utf-8'))
        # print(self.password)
        self.password = bcrypt.generate_password_hash(password)
        # self.password = bcrypt.generate_password_hash(str(password))
        # print(self.password)
        # self.password = password
        # print(self.password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        # Due to a weird pycharm bug, or perhaps dependency issue with python environment, it may sometimes falseley state that 'unicode' is not a valid reference.
        return self.id

    def __repr__(self):
        return '<user id: {}>'.format(self.id)


class Modules(db.Model):
    __tablename__ = 'modules'

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


class Roles(db.Model):
    __tablename__ = 'roles'
    # - admin role permissions
    # 	- role (pk)  /  permission name / r / w / u / d
    # - custom admin permissions
    # 	- id # / permission name  / r / w / u / d
    role = db.Column(db.String(20), primary_key=True)
    module_abbreviation = db.Column(db.String(3), primary_key=True)

    def __init__(self, role, module_abbreviation):
        self.role = role
        self.module_abbreviation = module_abbreviation

    def __repr__(self):
        return '<role/module: {}/{}>'.format(self.role, self.module_abbreviation)


class Permissions(db.Model):
    __tablename__ = 'permissions'
    # 	- table (user id #  /  group name  /  read  /  write  /  update  / delete
    # - need a relationship here with roles
    id = db.Column(db.Integer, primary_key=True)
    # role = db.Column(db.String(20), foreign_key=True)
    # module = db.Column(db.String(3), foreign_key=True)
    role = db.Column(db.String(20))
    module = db.Column(db.String(3))
    permission = db.Column(db.String(80), nullable=False)
    read = db.Column(db.Boolean, nullable=False)
    write = db.Column(db.Boolean, nullable=False)
    update = db.Column(db.Boolean, nullable=False)
    delete = db.Column(db.Boolean, nullable=False)

    def __init__(self, role, module, permission, r, w, u, d):
        self.role = role
        self.module = module
        self.permission = permission
        self.read = r
        self.write = w
        self.update = u
        self.delete = d

    def __repr__(self):
        return '<role/module permission: {}/{} {}>'.format(self.role, self.module, self.permission)


class Messages(db.Model):
    __tablename__ = 'messages'

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


class AppNotifications(db.Model):
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


class Contacts(db.Model):
    __tablename__ = 'contacts'

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


# # # CRM Models # # #
class Customers(db.Model):
    __tablename__ = 'customers'

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


class Agencies(db.Model):
    __tablename__ = 'agencies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    abbreviation = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<agency name: {}>'.format(self.id)


# # # HRM Models # # #
class Personnel(db.Model):
    __tablename__ = 'personnel'

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


# # # Marketing Models # # #
# - Linguistic analysis sub-module models.
class Result(db.Model):
    __tablename__ = 'results'

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
