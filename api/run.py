from flask import Flask
from flask_restful import Api
from resources.users import UserResource

def create_app(filename):
    """
    The method creates a flask app
    """
    app = Flask(__name__)
    app.config.from_object(filename)
    api = Api(app)

    api.add_resource(UserResource, '/user', '/user/', '/todo/<string:id>', '/todo/<string:id>/')

    return app

if __name__ == '__main__':
    app = create_app('config')
    app.run(debug=True)
