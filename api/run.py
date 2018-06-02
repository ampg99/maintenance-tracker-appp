import os
from flask import Flask, jsonify
from flask_restful import Api
from users import UsersRegisterResource, UserResource
from requests import RequestsListResource, RequestResource
from app import Testing

def create_app(filename):
    """The method creates a flask app"""
    app = Flask(__name__)
    app.config.from_object(filename)
    app.config.update(dict(
        TESTING = True,
        DEBUG=True,
        SECRET_KEY=os.urandom(24),
        USERNAME='admin',
        PASSWORD='default'
    ))

    api = Api(app)

    api.add_resource(UsersRegisterResource, '/api/v1/users', '/api/v1/users/', endpoint='get_users')
    api.add_resource(UserResource, '/api/v1/users/<int:user_id>', endpoint='get_one_user')
    api.add_resource(UserResource, '/api/v1/users/<int:user_id>', endpoint='delete_user')
    api.add_resource(UserResource, '/api/v1/users/<int:user_id>', endpoint='update_user')
    api.add_resource(UserResource, '/api/v1/users', endpoint='create_user')
    api.add_resource(RequestsListResource, '/api/v1/users/<int:user_id>/requests', '/api/v1/requests/', endpoint='get_requests')
    api.add_resource(RequestResource, '/api/v1/users/<int:user_id>/requests/<int:id>', endpoint='get_one_request')
    api.add_resource(RequestResource, '/api/v1/users/<int:user_id>/requests/<int:id>', endpoint='update_request')
    api.add_resource(RequestResource, '/api/v1/users/<int:user_id>/requests/<int:id>', endpoint='delete_request')
    api.add_resource(RequestResource, '/api/v1/users/<int:user_id>/requests', endpoint='create_request')


    return app

if __name__ == '__main__':
    app = create_app('config')
    app.run(debug=True)
