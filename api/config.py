
import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    JWT_SECRET_KEY = "my_awesome_key"
    TESTING = False
    USERNAME = "admin"
    PASSWORD = "barryazah"
    EMAIL = "asheuh4@gmail.com"
    MAIL_SERVER = 'smtp.mandrillapp.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'zhuxuefeng1994@126.com'
    MAIL_PASSWORD = 'GP4r-n8kVAILVe8NepkenQ'
    MAIL_DEFAULT_SENDER = 'flaskAPI@github.com'

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    JWT_SECRET_KEY = "my_awesome_key"

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'DEVELOPMENT': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}

default_config = app_config['DEVELOPMENT']