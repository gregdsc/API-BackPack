import os
#from source.configuration.database_url import DB_URI

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'I7QkQImQ6468QJkKQJ434QHJHFLSssjd'
    #SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SSL_REDIRECT = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'SSL0.OVH.NET')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_USE_TLS = int(os.environ.get('MAIL_USE_TLS', False))
    MAIL_USE_SSL = int(os.environ.get('MAIL_USE_SSL', True))
    EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    ADMINS = ['alexandre.pape@epitech.eu']
    TEST = '[TEST]'

    @staticmethod
    def init_app(app):
        pass

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
