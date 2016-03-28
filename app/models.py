from app import db, bcrypt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

db.Base = declarative_base()

user_messages = db.Table('user_messages', db.Base.metadata,
    db.Column('user_id', db.Integer, ForeignKey('user.id')),
    db.Column('messages_id', db.Integer, ForeignKey('messages.id'))
)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    groups = db.Column(db.String(500))
    permissions = db.Column(db.String(500))
    sent_messages = relationship("Messages", backref="user")
    # received_messages = relationship("Messages", backref="user")
    received_messages = relationship(
        "messages",
        secondary=user_messages,
        back_populates="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_has(password)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String())
    # Type examples: UserMessages, Notifications, Tasks, etc.
    subcategory = db.Column(db.String())
    # Subcategory examples: News, updates, etc.
    title = db.Column(db.String())
    body = db.Column(db.String())
    author = db.Column(db.String())
    delivery_methods = db.Column(db.String())
    # Delivery Method examples: To webapp, native app, push notification, SMS, e-mail, phone call, etc.
    notes = db.Column(db.String())
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    # destinations = db.Column(db.String())
    # Destinations examples: To users, groups.
    destinations = relationship(
        "user",
        secondary=user_messages,
        back_populates="messages")

    def __init__(self, type, subcategory, title, body, author, destinations, delivery_methods, notes):
        self.type = type
        self.subcategory = subcategory
        self.title = title
        self.body = body
        self.author = author
        self.destinations = destinations
        self.delivery_methods = delivery_methods
        self.notes = notes

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)
