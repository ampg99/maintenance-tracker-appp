import hashlib
import re
import pprint
import psycopg2.extras
from flask import request
from .models import User, MainModel
from passlib.handlers.bcrypt import bcrypt
from psycopg2.extensions import adapt, register_adapter, AsIs
from flask import jsonify
from .connectdb import Connection

class UserMixing:
    
    def __init__(self):
        self.conn = Connection()
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def get_all_users(self):
        self.cur.execute("SELECT * FROM mt_users;")
        # for row in self.cur:
        data = self.cur.fetchall()
            # data.append(row)
        return data

    def get_all_with_equal_fields(self, field, value):
        result = []
        for item in self.data.values():
            if item.json_obj()[field] == value:
                result.append(item)

        return result

    def adapt_user(self, user):
        username = adapt(user.username).getquoted()
        email = adapt(user.email).getquoted()
        password = adapt(user.password).getquoted()

        return AsIs("'(%s, %s, %s)'" % (username, email, password))
    def insert(self, user):
        assert isinstance(user, MainModel)
        try:
            query = ("INSERT INTO mt_users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);")
            print(user.to_json())
            self.cur.execute(query, (user.to_json()))
            self.conn.commit()
        except Exception as e:
            print(e)

    def set(self, user, user_id):
        assert isinstance(user, MainModel)
        a_user = self.get_all_users() 
        a_user[user_id] = user

    def get_user_by_id(self, user_id):
        data = self.get_all_users()
        return data.get(user_id)

    def gey_by_field(self, field, value):
        if self.get_all_users() is None:
            return {}
        for item in self.get_all_users():
            if item[field] == value:
                return item

    def remove(self, user_id):
        """Deletes a item withe the specified id"""
        user = self.get_all_users()
        del user[user_id]

class UserStore(UserMixing):
    """
    Document for a user's account information
    """
    
    def insert(self, user):
        assert isinstance(user, User)
        user.password = bcrypt.encrypt(user.password)

        # now insert item
        super().insert(user)
        
    def hash_password(self, password):
        """
        crypt the raw password and store it into database
        """
        item.password = hashlib.sha224(item.password).hexdigest()

    def is_valid(self, user):

        errors = {}
        
        if not user.get("email"):
            errors['email'] = "Please provide an email address"
        elif re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', user.get("email")) is None:
            errors["email"] = "Not a valid email"
        elif self.gey_by_field(field="email", value=user.get("email")) is not None:
            errors["email"] = "The email provided is being used by another user"

        if not user.get("password"):
            errors["password"] = "Please provide a password for this field"

        if not user.get("username"):
            errors['username'] = "Please provide a username"
        elif self.gey_by_field(field="username", value=user.get("username")) is not None:
            errors['username'] = "The user with the username already exits, choose another"


        return len(errors) == 0, errors
    
class Requests(UserMixing):
    
    def is_valid(self, request):
        errors = {}
        if not request.get("requestname"):
            errors["requestname"] = "Request must be given"

        if not request.get("description"):
            errors["description"] = "Description should be given"

        return len(errors) == 0, errors