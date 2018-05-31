from flask import Flask
from flask_restful import Api
from resources.users import RequestsListResource, RequestResource
from app import Testing

def create_app(filename):
    """
    The method creates a flask app
    """
    app = Flask(__name__)
    app.config.from_object(filename)
    api = Api(app)
    api.add_resource(RequestsListResource, '/api/v1/requests', endpoint='requests')
    api.add_resource(RequestResource, '/api/v1/requests/<int:id>', endpoint='request_id')
    api.add_resource(Testing, '/')

    return app

if __name__ == '__main__':
    app = create_app('config')
    app.run(debug=True)
