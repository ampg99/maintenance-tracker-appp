
import os

class Configuration:
    DEBUG = False
    CSRF_ENABLED = True
    JWT_SECRET_KEY = "flask runs"
    TESTING = False
    USERNAME = "admin"
    PASSWORD = "barryazah"
    EMAIL = "asheuh4@gmail.com"

class Development(Configuration):
    DEBUG = True


class Production(Development):
    pass


class Testing(Development):
    TESTING = True


config = {
    "TESTING": Testing,
    "DEVELOPMENT": Development,
    "PRODUCTION": Production
}

default_config = config['DEVELOPMENT']