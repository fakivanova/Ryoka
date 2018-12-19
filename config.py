import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or '332!!fj.,;@Ff@1;9(2fjv'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    FLASK_DEBUG = 1

    SQLALCHEMY_RECORD_QUERIES = True

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    SQLALCHEMY_DATABASE_URI = (os.environ.get('DEV_DATABASE_URL') 
                               or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))

class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = (os.environ.get('TEST_DATABASE_URL') 
                               or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite'))

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}
