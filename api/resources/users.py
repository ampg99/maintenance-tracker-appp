from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'asheuh':
        return 'barryazah'
    return None


@auth.error_handler
def unauthorized():
    """
    This returns false for non logged in users with the message access denied
    """
    return make_response(jsonify({'message': 'access denied'}), 403)

requests = []
users = []

class RequestsListResource(Resource):
    """ The class creates two end points , get_all_requests and create request """
    decorators = [auth.login_required]

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('requestname', type=str, required=True,
                                   help='No input privided for the request name',
                                   location='json')
        self.parse.add_argument('description', type=str, default="No description",
                                   location='json')
        super(RequestsListResource, self).__init__()
        self.request_fields = {
            'requestname': fields.String,
            'description': fields.String,
            'uri': fields.Url('get_requests')
        }

    def get(self):
        """
        The method gets all the requests
        """
        return {'requests': [marshal(req, self.request_fields) for req in requests]}, 200

    def post(self):
        """ 
        Method creates a new request
        """
        args = self.parse.parse_args()
        if requests == []:
            req = {
                'id': 1,
                'requestname': args['requestname'],
                'description': args['description']
            }
            requests.append(req)
        else:
            req = {
                'id': requests[-1]['id'] + 1,
                'requestname': args['requestname'],
                'description': args['description']
            }
            requests.append(req)
        return {'new_request': marshal(req, self.request_fields)}, 201


class RequestResource(Resource):
    """ The class creates threes endpoints, update request, delete request and get a single request """
    decorators = [auth.login_required]

    def __init__(self):
        self.parse2 = reqparse.RequestParser()
        self.parse2.add_argument('title', type=str, location='json')
        self.parse2.add_argument('description', type=str, location='json')
        self.request_fields = {
            'requestname': fields.String,
            'description': fields.String,
            'uri': fields.Url('get_one_request')
        }

        super(RequestResource, self).__init__()

    def get(self, id):
        req = [req for req in requests if req['id'] == id]
        if len(req) == 0:
            abort(404)
        return {'req': marshal(req[0], self.request_fields)}, 200

    def put(self, id):
        req = [req for req in self.request_fields if req['id'] == id]
        if len(req) == 0:
            abort(404)
        req = req[0]
        args = self.parse2.parse_args()
        for k, v in args.items():
            if v is not None:
                req[k] = v
        return {'req': marshal(req, self.request_fields)}, 200

    def delete(self, id):
        req = [req for req in requests if req['id'] == id]
        if len(req) == 0:
            abort(404)
        requests.remove(req[0])
        return {'result': True}


class UsersListResource(Resource):
    """ The class creates two end points , get_all_requests and create request """
    
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('username', type=str, required=True,
                                   help='No input privided for the username',
                                   location='json')
        self.parse.add_argument('email', type=str, default="",
                                   location='json')
        super(UsersListResource, self).__init__()
        self.user_fields = {
            'username': fields.String,
            'email': fields.String,
            'password': fields.String,
            'uri': fields.Url('get_users')
        }

    def get(self):
        """
        The method gets all the requests
        """
        return {'requests': [marshal(user, self.user_fields) for user in users]}, 200

    def post(self):
        """ Method creates a new request """
        args = self.parse.parse_args()
        if users == []:
            user = {
                'id': 1,
                'username': args['username'],
                'email': args['email'],
                'password': args['password']
            }
            users.append(user)
        else:
            user = {
                'id': requests[-1]['id'] + 1,
                'username': args['username'],
                'email': args['email'],
                'password': args['password']
            }
            requests.append(user)
        return {'new_user': marshal(user, self.user_fields)}, 201


class UserResource(Resource):
    """
    The class creates threes endpoints, update request, delete request and get a single request
    """

    def __init__(self):
        self.parse2 = reqparse.RequestParser()
        self.parse2.add_argument('username', type=str, location='json')
        self.parse2.add_argument('email', type=str, location='json')
        self.parse2.add_argument('password', type=str, location='json')
        self.request_fields = {
            'username': fields.String,
            'email': fields.String,
            'password': fields.String,
            'uri': fields.Url('get_one_request')
        }

        super(UserResource, self).__init__()

    def get(self, id):
        req = [req for req in requests if req['id'] == id]
        if len(req) == 0:
            abort(404)
        return {'req': marshal(req[0], self.request_fields)}, 200

    def put(self, id):
        req = [req for req in self.request_fields if req['id'] == id]
        if len(req) == 0:
            abort(404)
        req = req[0]
        args = self.parse2.parse_args()
        for k, v in args.items():
            if v is not None:
                req[k] = v
        return {'req': marshal(req, self.request_fields)}, 200

    def delete(self, id):
        req = [req for req in requests if req['id'] == id]
        if len(req) == 0:
            abort(404)
        requests.remove(req[0])
        return {'result': True}