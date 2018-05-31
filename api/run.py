from flask import Flask, jsonify
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
    
    api.add_resource(RequestsListResource, '/api/v1/requests', endpoint='get_requests')
    api.add_resource(RequestResource, '/api/v1/requests/<int:id>', endpoint='get_one_request')
    api.add_resource(RequestResource, '/api/v1/requests/<int:id>', endpoint='update_request')
    api.add_resource(RequestResource, '/api/v1/requests/<int:id>', endpoint='delete_request')
    api.add_resource(RequestsListResource, '/api/v1/requests', '/api/v1/requests/', endpoint='create_request')
    api.add_resource(Testing, '/')
    
    @app.route('/ping')
    def ping():
        return jsonify(ping='pong')

    return app

if __name__ == '__main__':
    app = create_app('config')
    app.run(debug=True)
