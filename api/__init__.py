from flask import Flask
from flask_restful import Api
from flask_restful.utils import cors
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from .model import initial
from .resources.userAPI import USER
from flask_sqlalchemy import SQLAlchemy

# local import
from .config import app_config

def create_app(config_name):

    # load configuration and bootstrap flask
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    mail = Mail(app)
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_token(token):
        """check if the token is blacklisted"""
        return token['jti'] in initial.db.blacklist
    api = Api(app)
    api.decorators = [cors.crossdomain(origin='*',
                                    headers='my-header, accept, content-type, token')]

    
    # add endpoints to flask restful api 
    # app.register_blueprint(admin, url_prefix="/api/v1/admin")
    app.register_blueprint(USER, url_prefix="/api/v1/users")

    return app
