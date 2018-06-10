from flask import Flask, jsonify
from flask_restful import Api
from flask_restful.utils import cors
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from .model import initial
from .model.models import RevokedTokenModel
from .resources.views import auth_blueprint
# local import
from .config import config

def create_app(config_name="DEVELOPMENT"):

    # load configuration and bootstrap flask
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    api = Api(app)

    jwt = JWTManager(app)

    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)

    # add endpoints to flask restful api

    #app.register_blueprint(admin, url_prefix="/api/v1/admin")
    app.register_blueprint(auth_blueprint, url_prefix="/api/v1/users")

    return app
