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

class RequestsListResource(Resource):
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
            'title': fields.String,
            'description': fields.String,
            'done': fields.Boolean,
            'uri': fields.Url('req')
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
        req = {
            'id': requests[-1]['id'] + 1,
            'requestname': args['title'],
            'description': args['description']
        }
        requests.append(req)
        return {'request1': marshal(req, self.request_fields)}, 201


class RequestResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.parse2 = reqparse.RequestParser()
        self.parse2.add_argument('title', type=str, location='json')
        self.parse2.add_argument('description', type=str, location='json')
        self.request_fields = {
            'title': fields.String,
            'description': fields.String,
            'done': fields.Boolean,
            'uri': fields.Url('req')
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