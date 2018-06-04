from flask_redis import Redis
from flask import current_app
from datetime import datetime
import json
from marshmallow import Schema, fields, validate
from api.config import default_config
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer)


STATUS_APPROVED = "Approved"
STATUS_REJECTED = "Rejected"
STATUS_RESOLVED = "Resolved"


class MainModel:

    def __init__(self):
        self.id = 0

    def to_json_object(self, exclude=True):
        return json.loads(self.to_json_str(exclude))

    def to_json_str(self, exclude=True):
        fields = self.excluded_fields()
        if not exclude:
            fields = []
        return json.dumps(self,
                          default=lambda o: o.strftime("%Y-%m-%d %H:%M:%S") if isinstance(o, datetime)
                          else {k: v for k, v in o.__dict__.items() if
                                k not in fields})

    def excluded_fields(self):
        return ['created_at', 'updated_at']



class User(MainModel):

    
    ADMIN_ROLE = "Administrator"
    USER_ROLE = "User"

    def __init__(self, username="", email="",  password=""):

        self.username = username
        self.email = email
        self.password = password
        self.role = User.USER_ROLE

    def __repr__(self):
        return '<User(username={self.__username!r})>'.format(self=self)

class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True,validate=validate.Email(error="Not a valid email"))
    password = fields.String(required=True)

class SuperUser(User):

    def __init__(self, username="", email="", password=""):
        #super(__class__, self).__init__(username, email, password)
        self.role = User.ADMIN_ROLE

    @staticmethod
    def admin_details():
        admin = SuperUser()
        admin.email = default_config.EMAIL
        admin.username = default_config.USERNAME
        admin.password = default_config.PASSWORD

        return admin


class AdminSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True,validate=validate.Email(error="Not a valid email"))
    password = fields.String(required=True)


class Request(MainModel):

    def __init__(self, requestname="", description="", created_by=None,
                 created_at=datetime.now(), updated_at=datetime.now(), status=None):
        super().__init__(created_date, updated_data)
        self.requestname = requestname
        self.description = description
        self.status = status
        self.created_by = created_by

    def excluded_fields(self):
        return ['updated_date']