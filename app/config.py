import os
import string
import random


##############
# - Super Classes
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # try:
    #     SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # except KeyError as e:
    #     print('{}: Database URI could not be loaded into memory. This is normal if running local scripts.'.format(e))


##############
# - Classes
class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False


##############
# - Functions
# - Description: Used to generate a random string of characters for the purpose of making a secret key.
def sk_generator(size=24, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
