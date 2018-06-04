import hashlib
import re
from .models import User, MainModel
from passlib.handlers.bcrypt import bcrypt
from flask import jsonify

class UserMixing:

    def __init__(self):
        self.data = {}
        self.index = 1

    def query_all(self):
        return self.data

    def query_all_where_field_eq(self, field, value):
        result = []
        for item in self.data.values():
            if item.to_json_object()[field] == value:
                result.append(item)

        return result

    def insert(self, item):
        assert isinstance(item, MainModel)
        self.data[self.index] = item
        item.id = self.index
        self.index += 1

    def set(self, item, item_id):
        assert isinstance(item, MainModel)
        self.data[item_id] = item

    def query(self, item_id):
        return self.data.get(item_id)

    def query_by_field(self, field, value):
        for item in self.data.values():
            if item.to_json_object()[field] == value:
                return item

    def remove(self, item_id):
        del self.data[item_id]

    def is_valid(self, item):
        return True, []

    def tear(self):
        self.data = {}

class UserStore(UserMixing):
    """
    Document for a user's account information
    """
    
    def insert(self, item):
        assert isinstance(item, User)
        item.password = bcrypt.encrypt(item.password)

        # now insert item
        super().insert(item)
        
    def hash_password(self, password):
        """
        crypt the raw password and store it into database
        """
        item.password = hashlib.sha224(item.password).hexdigest()

    def is_valid(self, item):

        errors = {}
        
        if not item.get("email"):
            errors['email'] = "Please provide an email address"
        elif re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', item.get("email")) is None:
            errors["email"] = "Not a valid email"
        elif self.query_by_field(field="email", value=item.get("email")) is not None:
            errors["email"] = "The email provided is being used by another user"

        if not item.get("password"):
            errors["password"] = "Please provide a password for this field"

        if not item.get("username"):
            errors['username'] = "Please provide a username"
        elif self.query_by_field(field="username", value=item.get("username")) is not None:
            errors['username'] = "The user with the username already exits, choose another"


        return len(errors) == 0, errors

class Requests(UserMixing):
    
    def is_valid(self, item):
        errors = {}
        if not item.get("product_name"):
            errors["product_name"] = "Product name must be provided"

        if not item.get("description"):
            errors["description"] = "Maintenance/Repair request description must be provided"

        return len(errors) == 0, errors