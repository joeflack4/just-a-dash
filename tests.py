# import os
from app import app, db
from app.models import User
from app.config import Config
# from flask import url_for
# from flask.ext.testing import TestCase
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
class TestCase(unittest.TestCase):
    # Setup/Teardown
    def setUp(self):
        Config.SQLALCHEMY_DATABASE_URI != ''
        # app.config['TESTING'] = True
        # app.config['WTF_CSRF_ENABLED'] = False
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        # - Note: This doesn't seem necessary.
        # db.create_all()
        self.test_users = [User(username='john', email='john@example.com', password='', admin_role='basic',
                                oms_role='basic', crm_role='basic', hrm_role='basic', mms_role='basic',
                                ams_role='basic')]

    def tearDown(self):
        db.session.remove()
        # - Note: This doesn't seem necessary.
        # db.drop_all()

    # Variables
    # test_users = [User(username='john', email='john@example.com', password='', admin_role='basic', oms_role='basic',
    #                    crm_role='basic', hrm_role='basic', mms_role='basic', ams_role='basic')]

    # Test Cases
    # def test_make_unique_username(self, users=test_users):
    def test_make_unique_username(self):
        # for user in users:
        for user in self.test_users:
            new_username = User.make_unique_username(user.username)
            new_unique_user = User(username=new_username, email='john2@example.com', password='', admin_role='basic',
                                   oms_role='basic', crm_role='basic', hrm_role='basic', mms_role='basic',
                                   ams_role='basic')
            db.session.add(new_unique_user)
            db.session.commit()
            new_username2 = User.make_unique_username(new_username)
            new_unique_comparison_user = User(username=new_username2, email='john3@example.com', password='',
                                              admin_role='basic', oms_role='basic', crm_role='basic', hrm_role='basic',
                                              mms_role='basic', ams_role='basic')
            db.session.add(new_unique_comparison_user)
            db.session.commit()
            assert new_username2 != new_username

            User.query.filter_by(username=new_username).delete()
            User.query.filter_by(username=new_username2).delete()
            db.session.commit()

    def test_avatar(self):
        for user in self.test_users:
            avatar = user.avatar(128)
            expected = 'http://www.gravatar.com/avatar/' + \
                'd4c74594d841139328695756648b6bd6'
            assert avatar[0:len(expected)] == expected

# class FlaskTestCase(unittest.TestCase):
#
#     # Ensures root routing loads correctly.
#     def test_index(self):
#         tester = app.test.client(self)
#         response = tester.get(url_for('root_path'), content_type='html/text')
#         self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
