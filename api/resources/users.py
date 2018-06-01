from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal

users = []

class UsersListResource(Resource):
    """ The class creates two end points , get_all_user and create user """

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
        return {'users': [marshal(user, self.user_fields) for user in users]}, 200

    def post(self):
        """Method creates a new user"""
        args = self.parse.parse_args()
        if users == []:
            user = {
                'user_id': 1,
                'username': args['username'],
                'email': args['email'],
                'password': args['password']
            }
            users.append(user)
        else:
            user = {
                'user_id': users[-1]['user_id'] + 1,
                'username': args['username'],
                'email': args['email'],
                'password': args['password']
            }
            users.append(user)
        return {'new_user': marshal(user, self.user_fields)}, 201


class UserResource(Resource):
    """The class creates threes endpoints, update user, delete user and get a single user"""

    def __init__(self):
        self.parse2 = reqparse.RequestParser()
        self.parse2.add_argument('username', type=str, location='json')
        self.parse2.add_argument('email', type=str, location='json')
        self.parse2.add_argument('password', type=str, location='json')
        self.user_fields = {
            'username': fields.String,
            'email': fields.String,
            'password': fields.String,
            'uri': fields.Url('get_one_user')
        }

        super(UserResource, self).__init__()

    def get(self, user_id):
        user = [user for user in users if user['user_id'] == user_id]
        if len(user) == 0:
            abort(404)
        return {'user': marshal(user[0], self.user_fields)}, 200

    def put(self, user_id):
        """ updates a user """
        user = [user for user in self.user_fields if user['user_id'] == user_id]
        if len(user) == 0:
            abort(404)
        user = user[0]
        args = self.parse2.parse_args()
        for k, v in args.items():
            if v is not None:
                user[k] = v
        return {'user': marshal(user, self.user_fields)}, 200

    def delete(self, user_id):
        """ deletes a user """
        user = [user for user in users if user['user_id'] == user_id]
        if len(user) == 0:
            abort(404)
        users.remove(user[0])
        return {'result': True}