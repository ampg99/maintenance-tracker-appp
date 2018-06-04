from flask import Flask
from flask_restful import Api
from flask_restful.utils import cors
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from .model import initial
from .resources.userAPI import USER
from flask_sqlalchemy import SQLAlchemy

# local import
from .config import config

def create_app(config_name="DEVELOPMENT"):
    
    # load configuration and bootstrap flask

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_token(token):
        """check if the token is blacklisted"""
        return token['jti'] in initial.db.blacklist
        
    # add endpoints to flask restful api 

    #app.register_blueprint(admin, url_prefix="/api/v1/admin")
    app.register_blueprint(USER, url_prefix="/api/v1/users")

    return app
