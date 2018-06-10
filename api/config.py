import os
class Configuration:
    DEBUG = False
    CSRF_ENABLED = True
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "i love hot ladies")
    TESTING = False
    BCRYPT_LOG_ROUNDS = 13
    USERNAME = "admin"
    PASSWORD = "barryazah"
    EMAIL = "asheuh4@gmail.com"

class Development(Configuration):
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


class Testing(Development):
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4


class Production(Configuration):
    DEBUG = False


config = {
    "TESTING": Testing,
    "DEVELOPMENT": Development
}

config_app = config['DEVELOPMENT']
