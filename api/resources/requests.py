from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal

requests = []

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None
class RequestsListResource(Resource):
    """ The class creates two end points , get_all_requests and create request """

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
            'uri': fields.Url('get_one_request')
        }

    def get(self):
        """The method gets all the requests"""
        return {'requests': [marshal(request, self.request_fields) for request in requests]}, 200

    def post(self):
        """  Method creates a new request"""
        args = self.parse.parse_args()
        if requests == []:
            request = {
                'id': 1,
                'requestname': args['requestname'],
                'description': args['description']
            }
            requests.append(request)
        else:
            request = {
                'id': requests[-1]['id'] + 1,
                'requestname': args['requestname'],
                'description': args['description']
            }
            requests.append(request)
        return {'new_request': marshal(request, self.request_fields)}, 201


class RequestResource(Resource):
    """ The class creates threes endpoints, update request, delete request and get a single request """

    def __init__(self):
        self.parse2 = reqparse.RequestParser()
        self.parse2.add_argument('requestname', type=str, location='json')
        self.parse2.add_argument('description', type=str, location='json')
        self.request_fields = {
            'requestname': fields.String,
            'description': fields.String,
            'uri': fields.Url('get_one_request')
        }

        super(RequestResource, self).__init__()

    def get(self, id):
        request = [request for request in requests if request['id'] == id]
        if len(request) == 0:
            abort(404)
        return {'request': marshal(request[0], self.request_fields)}, 200

    def put(self, id):
        request = [request for request in self.request_fields if request['id'] == id]
        if len(request) == 0:
            abort(404)
        request = request[0]
        args = self.parse2.parse_args()
        for k, v in args.items():
            if v is not None:
                request[k] = v
        return {'request': marshal(request, self.request_fields)}, 200

    def delete(self, id):
        request = [request for request in requests if request['id'] == id]
        if len(request) == 0:
            abort(404)
        requests.remove(request[0])
        return {'result': True}
