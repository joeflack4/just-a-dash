from app import app
from app.models import *
# from flask.ext.testing import TestCase as t
# import pytest
import unittest


# - Note: Testing implemented in flask testing extension; expirmentation.
# class BaseTestCase(t):
#     """A base test case."""
#
#     def create_app(self):
#         app.config.from_object('config.TestConfig')
#         return app
#
#     def setUp(self):
#         db.create_all()
#         # db.session.add(User("admin", "ad@min.com", "admin"))
#         # db.session.add(
#         #     BlogPost("Test post", "This is a test. Only a test.", "admin"))
#         db.session.commit()
#
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()


# - Note: Testing implemented in pytest; expirimentation.
# def f():
#     raise SystemExit(1)
#
# def test_mytest():
#     with pytest.raises(SystemExit):
#         f()


# - Note: Testing implemented in unittest.
