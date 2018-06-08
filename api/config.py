import os
class Configuration:
    DEBUG = False
    CSRF_ENABLED = True
    JWT_SECRET_KEY = "i love hot ladies"
    TESTING = False
    USERNAME = "admin"
    PASSWORD = "barryazah"
    EMAIL = "asheuh4@gmail.com"

class Development(Configuration):
    DEBUG = True


class Testing(Development):
    TESTING = True


class Production(Configuration):
    DEBUG = False


config = {
    "TESTING": Testing,
    "DEVELOPMENT": Development
}

config_app = config['DEVELOPMENT']
