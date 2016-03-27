from app import db
from sqlalchemy.dialects.postgresql import JSON


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


class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    # Type examples: UserMessages, Notifications, Tasks, etc.
    type = db.Column(db.String())
    # Subcategory examples: News, updates, etc.
    subcategory = db.Column(db.String())
    title = db.Column(db.String())
    body = db.Column(db.String())
    author = db.Column(db.String())
    # Destinations examples: To users, groups.
    destinations = db.Column(db.String())
    # Delivery Method examples: To webapp, native app, push notification, SMS, e-mail, phone call, etc.
    delivery_methods = db.Column(db.String())
    notes = db.Column(db.String())

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
