import unittest
import time
from flask import json
from ..model.initial import db
from ..model.models import User
from api import create_app

app = create_app()
client = app.test_client()

class TestAuthBlueprint(unittest.TestCase):
    def test_signup(self):
        """Test for user signup"""
        with client:
            response = client.post(
                'api/v1/users/auth/signup',
                data=json.dumps(dict(
                    username='bryan',
                    email='bryan@gmail.com',
                    password='edcp'
                )),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_register_with_already_registered_user_email(self):
        """Test signup with already registerd email """
        with client:
            response = client.post(
                'api/v1/users/auth/signup',
                data=json.dumps(dict(
                    username='hsshshsh',
                    email='paulla@gmail.com',
                    password='1234567'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_registered_user_login(self):
        """Test for login of registered user login"""
        with client:
            # registered user login

            response = client.post(
                'api/v1/users/auth/login',
                data=json.dumps(dict(
                    username='sella',
                    password=',m$$$'
                )),
                content_type='application/json'
            )
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_non_registered_user_login(self):
        """Test for login of non-registered useer"""
        with client:
            response = client.post(
                'api/v1/users/auth/login/access',
                data=json.dumps(dict(
                    username='paullette',
                    password='merjidjf'
                )),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 404)

    def test_valid_logout(self):
        """Test for logout before token expires"""
        with client:
            response_login = client.post(
                'api/v1/users/auth/login',
                data=json.dumps(dict(
                    username='sella',
                    password=',m$$$'
                )),
                content_type='application/json'
            )
            self.assertEqual(response_login.status_code, 404)

    def test_invalid_logout(self):
        """Test for logout before token expires"""
        with client:
            response_login = client.post(
                'api/v1/users/auth/login',
                data=json.dumps(dict(
                    username='sella',
                    password=',m$$$'
                )),
                content_type='application/json'
            )
            self.assertTrue(response_login.content_type == 'application/json')
            self.assertEqual(response_login.status_code, 404)


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
