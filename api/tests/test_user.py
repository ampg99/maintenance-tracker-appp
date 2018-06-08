import json
from flask import url_for
from api.model.models import User
from unittest import TestCase
from ..model import models

from api import create_app


main_url = "/api/v1/"

def setUp(self):
    self.app = create_app("TESTING")
    self.client = self.app.test_client
    self.headers = {'Content-Type': 'application/json'}
    self.superuser_headers = {'Content-Type': 'application/json'}
    self.admin = models.SuperUser()
    self.admin.username = "asheuh"
    self.admin.password = "barryazah"
    self.user = models.User()
    self.user.username = "mboya"
    self.user.email = "mboyabryan49@gmail.com"
    self.user.password = "123456789"
    self.client().post(
        url_for("users/auth/create_account"),
        data=self.user.json_str(False),
        headers=self.headers
    )

    result = self.client().post(
        url_for('users/auth/login'),
        data=self.user.json_str(False),
        headers=self.headers
    )
    json_result = json.loads(result.get_data(as_text=True))

    self.headers['Authorization'] = 'Bearer {}'.format(json_result['data']['token'])
    self.no_json_headers['Authorization'] = 'Bearer {}'.format(json_result['data']['token'])

def test_user_can_sign_up(self):
    result = self.client().post(url_for('users/auth/create_account'), headers=self.no_json_headers)
    self.assertEqual(result.status_code, 400)

    json_result = json.loads(result.get_data(as_text=True))
    self.assertEqual(json_result['message'], "Request should be in JSON")

    result = self.client().post(url_for('users/auth/create_account'), data=self.user.to_json_str(False),
                                headers=self.headers)
    json_result = json.loads(result.get_data(as_text=True))
    self.assertEqual(result.status_code, 201)  # Resource created

    self.assertEqual(json_result['status'], "success")

def test_user_cannot_sign_up_with_invalid_details(self):
    self.user.username = ""
    result = self.client().post(url_for('users/auth/create_account'), data=self.user.to_json_str(False),
                                headers=self.headers)
    json_result = json.loads(result.get_data(as_text=True))
    self.assertEqual(result.status_code, 400)  # Resource created

    self.assertEqual(json_result['status'], "error")
