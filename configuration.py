import os
import tempfile

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'I7QkQImQ6468QJkKQJ434QHJHFLSssjd' # var env
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SSL_REDIRECT = False
    #MAIL_SERVER = os.environ.get('MAIL_SERVER', 'SSL0.OVH.NET')
    #MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    #MAIL_USE_TLS = int(os.environ.get('MAIL_USE_TLS', False))
    #MAIL_USE_SSL = int(os.environ.get('MAIL_USE_SSL', True))
    #EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    #EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    ADMINS = ['alexandre.pape@epitech.eu']
    TEST = '[TEST]'

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        tempfile.gettempdir(), 'test.db')
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
