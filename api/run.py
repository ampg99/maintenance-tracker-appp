from flask import Flask
from flask_restful import Api
from resources.users import UserResource
from app import Testing

def create_app(filename):
    """
    The method creates a flask app
    """
    app = Flask(__name__)
    app.config.from_object(filename)
    api = Api(app)

    api.add_resource(Testing, '/')
    api.add_resource(UserResource, '/api/v1', '/api/v1/', '/api/v1/<string:id>', '/api/v1/<string:id>/')

    return app

if __name__ == '__main__':
    app = create_app('config')
    app.run(debug=True)
