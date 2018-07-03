class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DATABASE = "myway"


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = "myway"


class TestingConfig(Config):
    TESTING = True
    DATABASE = "myway_test"
