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
    SECRET_KEY = 'this-really-needs-to-be-changed'
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    
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


class TestingConfig(Config):
    TESTING = True
