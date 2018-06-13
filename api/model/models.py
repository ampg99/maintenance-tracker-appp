#! /usr/bin/python3
from flask_redis import Redis
from flask import current_app
import jwt
from psycopg2.extensions import adapt, register_adapter, AsIs
from flask import jsonify
import psycopg2.extras
from datetime import datetime, timedelta
import json
from api.config import config_app
from .connectdb import Connection, rollback
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer)

conn = Connection()


class MainModel:

    def json_obj(self, exclude=True):
        """Changes to response to json object"""
        return json.loads(self.json_str(exclude))

    def json_str(self, exclude=True):
        """changes the response to string value"""
        fields = self.fields_not_included()
        if not exclude:
            fields = []
        return json.dumps(self,
                          default=lambda o: o.strftime("%Y-%m-%d %H:%M:%S") if isinstance(o, datetime)
                          else {k: v for k, v in o.__dict__.items() if
                                k not in fields})

    def fields_not_included(self):
        """These are the items that are excluded from each field values"""
        return ['created_date', 'updated_date']



class User(MainModel):
    """The main user class that creates the user"""

    __tablename__ = "mt_users"
    ADMIN_ROLE = "Superuser"
    USER_ROLE = "User"

    def __init__(self, role, username="", email="", password="", registered_on=""):
        """Initializes the user details"""
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
        self.registered_on = datetime.now()
        self.role = User.USER_ROLE

    def __repr__(self):
        return '<User(username={self.__username!r})>'.format(self=self)
    
    def encode_auth_token(self, username):
        """
        Generates the auth Token
        :return: string
        """
        from api import create_app
        app = create_app()
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
            'iat': datetime.utcnow(),
            'sub': username
        }
        return jwt.encode(
            payload,
            app.config.get('JWT_SECRET_KEY'),
            algorithm='HS256'
        )

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: interger|string
        """
        from api import create_app
        app = create_app()
        try:
            payload = jwt.decode(auth_token, app.config.get('JWT_SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please login again.'

    def to_json(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role
        }

class SuperUser(User):
    """The superuser class for creating the admin"""

    def __init__(self, username="", email="", password=""):
        """Intializes the role of an admin"""
        super().__init__(username, email, password)
        self.role = User.ADMIN_ROLE

    @staticmethod
    def admin_details():
        """Provides the superuser details from the default admin configuration"""
        superuser = SuperUser()
        superuser.email = config_app.EMAIL
        superuser.username = config_app.USERNAME
        superuser.password = config_app.PASSWORD

        return superuser


class RevokedTokenModel(MainModel):
    __tablename__ = 'blacklist_tokens'

    def __init__(self, jti=''):
        self.jti = jti
        rollback(RevokedTokenModel)

    @classmethod
    def query_by_token(cls, _jti):
        
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM blacklist_tokens WHERE jti=%s"
        result = cursor.execute(query, (_jti,))
        row = cursor.fetchone()
        try:
            return row if row else None
        except Exception as e:
            print(e)
    
    def add(self):
        cursor = conn.cursor()

        query = "INSERT INTO blacklist_tokens (jti) values (%s)"
        cursor.execute(query, (self.jti))

        conn.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, _jti):
        query = cls.query_by_token(_jti = _jti)
        return bool(query)
