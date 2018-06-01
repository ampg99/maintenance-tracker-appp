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
    """This returns false for non logged in users with the message access denied"""
    return make_response(jsonify({'message': 'access denied'}), 403)

requests = []

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
        """The method gets all the requests"""
        return {'requests': [marshal(request, self.request_fields) for request in requests]}, 200

    def post(self):
        """  Method creates a new request"""
        args = self.parse.parse_args()
        if requests == []:
            request = {
                'request_id': 1,
                'requestname': args['requestname'],
                'description': args['description']
            }
            requests.append(request)
        else:
            request = {
                'request_id': requests[-1]['request_id'] + 1,
                'requestname': args['requestname'],
                'description': args['description']
            }
            requests.append(request)
        return {'new_request': marshal(request, self.request_fields)}, 201


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

    def get(self, request_id):
        request = [request for request in requests if request['request_id'] == request_id]
        if len(request) == 0:
            abort(404)
        return {'request': marshal(request[0], self.request_fields)}, 200

    def put(self, request_id):
        request = [request for request in self.request_fields if request['request_id'] == request_id]
        if len(request) == 0:
            abort(404)
        request = request[0]
        args = self.parse2.parse_args()
        for k, v in args.items():
            if v is not None:
                request[k] = v
        return {'request': marshal(request, self.request_fields)}, 200

    def delete(self, request_id):
        request = [request for request in requests if request['request_id'] == id]
        if len(request) == 0:
            abort(404)
        requests.remove(request[0])
        return {'result': True}