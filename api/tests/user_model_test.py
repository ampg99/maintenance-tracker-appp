from ..model.models import User
from ..model.initial import db
from unittest import TestCase

class TestUserModel(TestCase):
    def test_encode_auth_token(self):
        user = User(
            username="sella",
            email="sella@gmail.com",
            password="mermaid",
            role="user"
        )
        db.users.insert_test_tb(user)
        auth_token = user.encode_auth_token(user.username)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            username = "sella",
            email = "sella@gmail.com",
            password = "mermaid",
            role='user'
        )
        db.users.insert_test_tb(user)
        auth_token = user.encode_auth_token(user.username)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token) == user.username)