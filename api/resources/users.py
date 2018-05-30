from flask import json, request, abort, make_response, url_for, Flask
from flask_restful import Resource

requests = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

users = []
class UserResource(Resource):
    """
    The class creates a resource
    """
    def get(self):
        response = [user.json_dump() for user in users]
        return {"status": "success", "data": users}, 200

    def post(self):
        user = dict(
            id=4,
            username='asheuh',
            email='asheuh@gmail.com',
            password='1234567'
        )
        user.save()
        return {"status": "success", "data": user}, 201

    def put(self, id):
        users.first()
        users['username'] = 'brian'
        return{"status": "success", "data": users}, 200

    def delete(self, id):
        users['id'].delete()
        return {"status": "deleted", "data": users}, 200

class RequestsResource(Resource):
    """
    The class creates a resource
    """
    def get(self):

        """
        Creates the get all requests
        """
        return {'requests': requests}

    def get(self, id):
        """
        Creates the get a request (by id)
        """
        for req in requests:
            return req
        return {'request': req[0]}

    def post(self):
        myrequest = {
            'id': requests[-1]['id'] + 1,
            'title': request.json['title'],
            'description': request.json.get('description', ""),
            'done': False
        }
        requests.append(myrequest)
        return {'request': requests}, 201

    def put(self , id):
        request = filter(lambda t: t['id'] == id, requests)
        if len(request) == 0:
            abort(404)
        if not request.json:
            abort(400)
        if 'title' in request.json:
            abort(400)
        if 'description' in request.json:
            abort(400)
        if 'done' in request.json and type(request.json['done']) is not bool:
            abort(400)
        request[0]['title'] = request.json.get('title', request[0]['title'])
        request[0]['description'] = request.json.get('description', request[0]['description'])
        request[0]['done'] = request.json.get('done', request[0]['done'])
        return {'request': request[0]}

    def delete(self,  id):
        requests.remove(request[0])
        return  {'requests': requests}
