import unittest
import json
import pytest
from flask import url_for
from run import create_app
from resources.users import RequestsListResource, RequestResource

"""
Importing unittest moduke
"""

class TestEndpoints:
    """
    This i a class for the test case of user
    """
    def setUp(self):
        """
        The method does the initialization of variables for test case
        """
        app = create_app(filename="config")
        client = app.test_client()
        self.user = {
            'id': 1,
            'username': 'asheuh',
            'email': 'asheuh@gmail.com',
            'password': '1223456778'
        }

    def login(self, client, *args, **kwargs):
        """
        This method logs in the user
        """
        return client.post('/api/v1/login', data=dict(**kwargs), follow_redirects=True)

    def logout(self, client, *args):
        """
        This method logs out the user and redirects them to a page
        """
        return client.get('/api/v1/logout', follow_redirects=True)

    def test_user_post(self, client):
        """
        The method creates a user through an api
        """
        response = client.post(url_for('create_user'), data=self.user)
        assert response.status_code == 201

    def test_users_get(self, client):
        """
        The api test to see if it can get all users
        """
        response = client.get(url_for('get_users'))
        assert response.status_code == 200

    def test_user_put(self, client):
        """
        Api can perform update using PUT request
        """
        # data to be updated
        response = client.put(url_for('update_user'), data = {
            'username': 'mermaid',
            'email': 'paulla@gmail.com',
            'password': 'q0qq0q0q0qq0'
        })
        assert response.status_code == 200

    def test_user_get(self, client):
        """
        This method tells the api to get a single user
        """
        response = client.get(url_for('get_one_user'))
        assert response.status_code == 200
        assert response.json == self.user

    def test_user_delete(self, client):
        """
        The api can delete a user
        """
        response = client.delete(url_for('delete_user'))
        assert response.status_code == 200

    def test_request_post(self, client):
        """
        The user can create a request
        """
        response = client.post(url_for('create_request'), data=dict(
            Id=1,
            request_name="Internet connection",
            description="poor Internet connection on vpn",
            posted_date='1/21/2018'
        ), follow_redirects=True)
        assert response.status_code == 201

    def test_request_get(self, client):
        """
        The user can get and view all the requests with (GET request)
        """
        response = client.get(url_for('get_requests'))
        assert response.status_code == 200

    def test_request_by_id_get(self, client):
        """
        The user can get a single request and view it (with GET request)
        """
        response = client.get(url_for('get_one_request', id=1))
        assert response.status_code == 200

    def test_request_put(self, client):
        """
        The user can update a request with PUT request
        """
        response = client.put(url_for('update_request', id=1), data=dict(
            request_name="Malware",
            description="Hacked",
            posted_date='12/28/2018'
        ), follow_redirects=True)

        assert response.status_code == 200

    def test_request_delete(self, client):
        """
        The user can delete a request
        """
        response = client.delete(url_for('delete_request', id=1))
        assert response.status_code == 200

    def test_login(self, client):
        """
        The method test user log in with correct input
        """
        response = self.login(self, 'paulla@gmail.com', '12345678')
        assert b'You are now logged in' in response.data
        # Tests for Invalid user email input
        response = self.login(self, 'paulla@gmail.com' + 't', '12345678')
        assert b'Invalid email address' in response.data
        # Test for invalid user password input
        response = self.login(self, 'paulla@gmail.com', '12345678' + 't')
        assert b'Invalid password given' in response.data

    def test_logout(self):

        """
        The method test user log out and tells the user if they are logged out
        and then redirects them to a page
        """
        response = self.logout(self)
        assert b'You are now logged out' in response.data


class TestApp:
    
    def test_ping(self, client):
        res = client.get(url_for('ping'))
        assert res.status_code == 200
        assert res.json == {'ping': 'pong'}