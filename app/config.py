import os

#
# try:
#     app.config.from_object(os.environ['DATABASE_URL'])
#     print(os.environ['DATABASE_URL'])
# except KeyError as e:
#     os.environ["DATABASE_URL"] = 'postgresql+psycopg2://joeflack4:pizzaLatte186*@localhost/justadash'
#     app.config.from_object(config.DevelopmentConfig)
#     print(os.environ['DATABASE_URL'])
# except:
#     os.environ["DATABASE_URL"] = 'postgresql+psycopg2://joeflack4:pizzaLatte186*@localhost/justadash'
#     app.config.from_object(config.DevelopmentConfig)
#     print(os.environ['DATABASE_URL'])
#     pass

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    # SECRET_KEY = '\xa7\x16\x9b\x87\x80\x1aU&\x13Q\x1fL\xe7\xe1\x02\xb1\x19\xbfZ\xaa\x84\x8e;\x19'
    SECRET_KEY = '\xa7\x16\x9b\x87\x80\x1aU&\x13Q\x1fL\xe7\xe1\x02\xb1'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    # SQLALCHEMY_DATABASE_URI = os.environ['postgresql+psycopg2://joeflack4:pizzaLatte186*@localhost/justadash']
    # app.config['SQL_ALCHEMY_URI'] = 'postgresql+psycopg2://joeflack4:pizzaLatte186*@localhost/justadash'


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