class Config(object):
    DEBUG = False
    TESTING = False
    MAIL_SERVER = ''
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    ADMINS = ['']


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    MAIL_SERVER = ''
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_PORT = 465
    MAIL_USE_SSL = True
