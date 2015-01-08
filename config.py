class Config(object):
    DEBUG = False
    TESTING = False
    MAIL_SERVER = ''
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    ADMINS = ['pbeeson@thevariable.com']
    WUNDERGROUND_API_KEY = '82cd0bcb8cf21f67'
    WUNDERGROUND_BASE_URL = 'http://api.wunderground.com/api/'


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
