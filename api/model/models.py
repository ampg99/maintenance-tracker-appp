#! /usr/bin/python3
from flask_redis import Redis
from flask import current_app
from datetime import datetime
import json
from api import config
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer)


STATUS_APPROVED = "Approved"
STATUS_REJECTED = "Rejected"
STATUS_RESOLVED = "Resolved"


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

    ADMIN_ROLE = "Superuser"
    USER_ROLE = "User"

    def __init__(self, username="", email="", password=""):
        """Initializes the user details"""
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
        self.role = User.USER_ROLE

    def __repr__(self):
        return '<User(username={self.__username!r})>'.format(self=self)

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
        superuser.email = config.config_app.EMAIL
        superuser.username = config.config_app.USERNAME
        superuser.password = config.config_app.PASSWORD

        return superuser.to_json()


class Request(MainModel):
    """The class creates the request models"""

    def __init__(self, requestname="",
                 description="", created_by=None,
                 created_date=datetime.now(),
                 updated_date=datetime.now(),
                 status=None):
        self.requestname = requestname
        self.description = description
        self.status = status
        self.created_by = created_by
        super().__init__(created_date, updated_date)

    def fields_not_included(self):
        return ['updated_date']
