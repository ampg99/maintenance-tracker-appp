from flask import json, request
from flask_restful import Resource

class UserResource(Resource):
    """
    This class creates a user resource with GET POST PUT and DELETE
    """
    def __init__(self):
        self.users = dict()
        self.requests = dict()

    def get(self):
        return {'users': self.users}, 200

    def post(self):
        user = dict(
            Id=1,
            username='asheuh',
            email='asheuh@gmail.com',
            password='123567899'
        )
        self.users.update(user)
        return {'users': self.users}, 201
