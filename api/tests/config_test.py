"""import json
from flask import url_for
from api.model.models import User
from unittest import TestCase
from ..model import models

from api import create_app


main_url = "/api/v1/"
app = create_app("TESTING")
user = models.User()
admin = models.SuperUser()

def setUp():
    client = app.test_client
    headers = {'Content-Type': 'application/json'}
    superuser_headers = {'Content-Type': 'application/json'}
    admin.username = "asheuh"
    admin.password = "barryazah"
    user.username = "mboya"
    user.email = "mboyabryan49@gmail.com"
    user.password = "123456789"

    with app.test_request_context():
        client().post(
            url_for("users/auth/signup"),
            data=user.json_str(False),
            headers=headers
        )

    result = client().post(
        url_for('users/auth/login'),
        data=user.json_str(False),
        headers=headers
    )
    json_result = json.loads(result.get_data(as_text=True))

    headers['Authorization'] = '{}'.format(json_result['data']['token'])
    no_json_headers['Authorization'] = '{}'.format(json_result['data']['token'])

def test_user_can_sign_up():
    with app.test_request_context():
        result = client().post(url_for('users/auth/signup'), headers=no_json_headers)
        assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        assertEqual(json_result['message'], "Request should be in JSON")

        result = client().post(url_for('users/auth/signup'), data=user.json_str(False),
                                    headers=headers)
        json_result = json.loads(result.get_data(as_text=True))
        assertEqual(result.status_code, 201)
        assertEqual(json_result['status'], "success")

def test_invalid_details():
    with app.test_request_context():
        user.username = ""
        result = client().post(url_for('users/auth/signup'), data=user.json_str(False),
                                    headers=self.headers)
        json_result = json.loads(result.get_data(as_text=True))
        assertEqual(result.status_code, 400)

        assertEqual(json_result['status'], "error")
"""
from unittest import TestCase
from flask import current_app
from api.config import config
from api import create_app

app = create_app()

class TestDevelopmentConfig(TestCase):
    def create_app(self, config_name="DEVELOPMENT"):
        app.config.from_object(config[config_name])
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['JWT_SECRET_KEY'] is 'i love hot ladies')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)

class TestTestingConfig(TestCase):
    def create_app(self, config_name="DEVELOPMENT"):
        app.config.from_object(config[config_name])
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['JWT_SECRET_KEY'] is 'i love hot ladies')
        self.assertTrue(app.config['DEBUG'])