

class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = '12345'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:12345@localhost/BookOOPS"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
