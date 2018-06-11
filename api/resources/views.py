from flask import Blueprint, request, make_response, jsonify
from flask_restful import reqparse
import json
import pprint
from flask.views import MethodView
from passlib.handlers.bcrypt import bcrypt
from ..model.models import User, RevokedTokenModel
from ..model.initial import db
from flask_jwt_extended import (
    jwt_required, 
    create_access_token,
    create_refresh_token,
    get_jwt_identity, 
    get_raw_jwt,
    jwt_refresh_token_required
)
from functools import wraps
from ..model.models import User
from ..model.requests_models import RequestsModel
from ..model.connectdb import Connection

conn = Connection()
auth_blueprint = Blueprint('resources.views', __name__)
parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

@jwt_required
def get_current_user():
    return db.users.get_by_field("user_id", get_jwt_identity())

def admin_guard(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        user = get_jwt_identity()
        if not user.is_admin():
            return {"status": "error", "message": "User not an Admin"}, 401
        return f(*args, **kwargs)

    return wrapped

class SignupAPI(MethodView):
    """User signup resource authentication"""

    def post(self):
        # get user post data
        result = request.get_json()
        # check if any errors and check if user already exists
        user, errors = db.users.is_valid(result)
        if not errors:
            try:
                user = User(
                    username=result.get('username'),
                    email=result.get('email'),
                    password=result.get('password'),
                    role=result.get('role')
                )

                # insert the user

                db.users.insert(user)
                # generate the token for authentication
                auth_token = create_access_token(identity=user.username)
                refresh_token = create_refresh_token(identity = user.username)
                response = {
                    'status': 'success',
                    'message': 'Successfully signed up for an account',
                    'auth_token': auth_token,
                    'refreash_token': refresh_token,
                    'data': user.json_obj()
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {
                    'status': 'fail',
                    'message': 'An error occurred: {}'.format(e)
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'status': 'fail',
                'message': errors
            }
            return make_response(jsonify(response)), 200

class LoginAPI(MethodView):
    """User login resource authentication"""

    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            username, password = post_data.get('username').strip(), \
            post_data.get('password').strip()
        except Exception as e:
            resp = {
                "Status": "error",
                "Message": "Invalid credential, please provide right credential"
            }
            return make_response(jsonify(resp))

        user = db.users.get_by_field(
            "username", 
            request.json.get("username")
        )
        try:
            auth_token = create_access_token(identity=user['username'])
            refresh_token = create_refresh_token(identity = user['username'])
        except Exception as e:
            print(e)
        # auth_token = User.encode_auth_token(User, user['username'])
        if not user:
            response =  {
                "status": "fail", 
                "message": "Username does not exist"
            }
            return make_response(jsonify(response)), 404

        elif not bcrypt.verify(request.json.get("password"), user['password']):
            response =  {
                "status": "error", 
                "message": "The password you provided is wrong"
            }
            return make_response(jsonify(response)), 400
        elif not auth_token:
            response = {
                'status': 'error',
                'message': 'The token provided is incorrect'
            }
            return make_response(jsonify(response)), 400

        else:
            response = {
                'status': 'success',
                'message': 'successfully logged in',
                'auth_token': auth_token,
                'refresh_token': refresh_token,
                'user': user
            }
            return make_response(jsonify(response)), 200


class AllUsers(MethodView):
    """ Logged in user gets all the requests """
    def get(self):
        headers = {'Content_type': 'application/json'}
        all_users = db.users.get_all_users()
        response = {
            'All users': all_users
        }
        return jsonify(response)

    def put(self):
        pass


class LogoutAccessAPI(MethodView):
    """ Logout Resource for the user"""
    @jwt_required # Security authentication
    def post(self):
        # get token
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            response = {
                'status': 'success',
                'message': 'Access token has been revoked'
            }

            return make_response(jsonify(response))
        except:
            response = {'message': 'Something went wrong'}, 500
            return make_response(jsonify(response))


class LogoutRefreshAPI(MethodView):
    """ Logout Resource"""
    @jwt_refresh_token_required # Security authentication
    def post(self):
        # get token
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            response = {
                'status': 'success',
                'message': 'Access token has been revoked'
            }

            return make_response(jsonify(response))
        except:
            response = {'message': 'Something went wrong'}, 500
            return make_response(jsonify(response))


class TokenRefresh(MethodView):
    @jwt_refresh_token_required # Security authentication
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}




class RequestAPI(MethodView):
    """Requests Resources"""
    parser = reqparse.RequestParser()
    parser.add_argument('description',
                        type=float,
                        required=True,
                        help='This field cannot be left blank.')

    @jwt_required # Security authentication
    def post(self):
        """
        objective: POST an new item to item database.
        :param name: str - new item name
        :return: json - new item with status code
        """
        result = request.get_json()
        # check if any errors and check if user already exists
        req, errors = db.requests.is_valid(result)
        if not errors:
            try:
                my_request = RequestsModel(
                    requestname=result.get('requestname'),
                    description=result.get('description'),
                    owner=get_jwt_identity()
                )

                # insert the request

                my_request.insert(my_request)
                response = {
                    'status': 'success',
                    'message': 'Successfully sent a request',
                    'data': my_request.json()
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {
                    'status': 'fail',
                    'message': 'An error occurred: {}'.format(e)
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'status': 'fail',
                'message': errors
            }
            return make_response(jsonify(response)), 200



class AllRequests(MethodView):
    @jwt_required # Security authentication
    def get(self):
        headers = {'Content_type': 'application/json'}
        requests = RequestsModel.find_all(self)
        response = {
            'All requests': requests
        }
        return jsonify(response)


class RequestsById(MethodView):
    @jwt_required # Security authentication
    def get(self, request_id):
        """
        objective: GET an item from item database.
        :param name: str - item name
        :return: json - item with status code
        """

        item = RequestsModel.find_by_id(request_id)
        # user = get_jwt_identity()
        if not item:
            response = {
                'status': 'error', 
                'message': f'A request with the id {request_id} is not found.'
            }, 404
            return make_response(jsonify(response)), 404
        response = {'request': item}
        return make_response(jsonify(response)), 200

    @jwt_required # Security authentication
    def delete(self, request_id):
        """
        objective: DELETE an item from the item database.
        :param name: str - item name
        :return: json - status message
        """
        cursor = conn.cursor()

        query = "DELETE FROM mt_requests WHERE request_id=%s"
        cursor.execute(query, (request_id,))

        conn.commit()
        if not request_id:
            response = {
                'status': 'error',
                'message': f'Request with id {request_id} was not found.'
            }, 200
            return make_response(jsonify(response))
        else:
            response = {
                'status': 'success',
                'message': f'Request with id {request_id} deleted.'
            }, 200
            return make_response(jsonify(response))

    @jwt_required # Security authentication
    def put(self, request_id):
        """
        objective: PUT an item into the in-memory database store. If the
                   item exists, update its contents.
        :param name: str - item name
        :return: json - item
        """
        item = RequestsModel.find_by_id(request_id)
        print(item)
        if not request_id:
            response = {
                'status': 'error',
                'message': f'Request with id {request_id} was not found.'
            }, 200
            return make_response(jsonify(response))
        else:
            result = request.json
            req, errors = db.requests.is_valid(result)
            if errors:
                response = {
                    "status": "error",
                    "message": errors
                }
                return make_response(jsonify(response))

            item['requestname'] = result['requestname']
            item['description'] = result['description']
        
            item.update()
            response = {
                'status': 'success',
                'message': 'Request updated successfuly',
                'Updated': item
            }, 200
            return make_response(jsonify(response))
            

# define the API resources
signup_view = SignupAPI.as_view('signup')
login_view = LoginAPI.as_view('login')
all_view = AllUsers.as_view('users')
logout_view_access = LogoutAccessAPI.as_view('logout_api')
logout_view_refresh = LogoutRefreshAPI.as_view('logout_api')
request_view = RequestAPI.as_view('request_apoi')
allrequest_view = AllRequests.as_view('requests')
requestbyid_view = RequestsById.as_view('requestid_api')

# Add rules for API endpoints
auth_blueprint.add_url_rule(
    '/auth/signup',
    view_func=signup_view,
    methods=['POST',]
)

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST',]
)

auth_blueprint.add_url_rule(
    '/',
    view_func=all_view,
    methods=['GET',]
)

auth_blueprint.add_url_rule(
    '/auth/logout/access',
    view_func=logout_view_access,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/auth/logout/refresh',
    view_func=logout_view_access,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/requests',
    view_func=request_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/requests',
    view_func=allrequest_view,
    methods=['GET',]
)
auth_blueprint.add_url_rule(
    '/requests/<int:request_id>',
    view_func=requestbyid_view,
    methods=['GET',]
)

auth_blueprint.add_url_rule(
    '/requests/<int:request_id>',
    view_func=requestbyid_view,
    methods=['DELETE',]
)

auth_blueprint.add_url_rule(
    '/requests/<int:request_id>',
    view_func=requestbyid_view,
    methods=['PUT',]
)