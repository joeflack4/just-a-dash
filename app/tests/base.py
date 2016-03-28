from flask.ext.testing import TestCase

from app import app, db
from app.models import *


class BaseTestCase(TestCase):
    """A base test case."""

    # def create_app(self):
    #     app.config.from_object('config.TestConfig')
    #     return app
    #
    # def setUp(self):
    #     db.create_all()
    #     db.session.add(User("admin", "ad@min.com", "admin"))
    #     db.session.add(
    #         BlogPost("Test post", "This is a test. Only a test.", "admin"))
    #     db.session.commit()
    #
    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
