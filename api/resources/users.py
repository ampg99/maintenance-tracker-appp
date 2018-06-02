from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask import Flask, render_template, flash, request, url_for, redirect, session
from passlib.hash import sha256_crypt

USERS = []


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
    
class UsersRegisterResource(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('username', type=str, required=True,
                                    help='No input privided for the username',
                                    location='json')
        self.parse.add_argument('email', type=str, default="",
                                    location='json')
        super(UsersRegisterResource, self).__init__()
        self.user_fields = {
            'username': fields.String,
            'email': fields.String,
            'password': fields.String,
            'uri': fields.Url('get_one_user')
        }

    def get(self):
        return {'users': [marshal(user, self.user_fields) for user in USERS]}, 200

    def post(self):
        user = self.user_fields
        args = self.parse.parse_args()
        if request.method == "POST":
            
            if USERS == []:
                user = {
                    'user_id': 1,
                    'username': args['username'],
                    'email': args['email'],
                    'password': sha256_crypt.encrypt((str(user['password'])))
                }
                USERS.append(user)

            else:
                for user in USERS:
                    if user['username'] in user.values():
                        return {'message': 'That username is already taken, please choose another'}
                    else:
                        user = {
                            'user_id': USERS[-1]['user_id'] + 1,
                            'username': user['username'],
                            'email': user['email'],
                            'password': sha256_crypt.encrypt((str(user['password'])))
                        }
                        USERS.append(user)
                        return redirect(url_for('get_one_user'))
            return {'new_user': marshal(user, self.user_fields)}, 201


class UserResource(Resource):
    """"The class creates threes endpoints, update user, delete user and get a single user"""

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
        user = [user for user in USERS if user['user_id'] == user_id]
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
        user = [user for user in USERS if user['user_id'] == user_id]
        if len(user) == 0:
            abort(404)
        USERS.remove(user[0])
        return {'result': True}
