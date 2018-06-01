import unittest
import json
import pytest
from flask import url_for
from run import create_app

app = create_app('config')

@pytest.fixture
def client(request):
    app.config['TESTING'] = True
    client = app.test_client()

    return client

def login(client, username, password):
    """This method logs in the user"""
    client = client(client)
    return client.post('/api/v1/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    """This method logs out the user and redirects them to a page"""
    client = client(client)
    return client.get('/api/v1/logout', follow_redirects=True)

class TestEndpoints:
    """ This i a class for the test case of user """
    def setUp(self):
        """The method does the initialization of variables for test case """
    @pytest.fixture
    def test_login_logout(self, client):
        """Make sure login and logout works"""
        rv = login(client, app.config['USERNAME'],
               app.config['PASSWORD'])
        assert b'You were logged in' in rv.data
        rv = logout(client)
        assert b'You were logged out' in rv.data
        rv = login(client, app.config['USERNAME'] + 'x',
            app.config['PASSWORD'])
        assert b'Invalid username' in rv.data
        rv = login(client, app.config['USERNAME'],
            app.config['PASSWORD'] + 'x')
        assert b'Invalid password' in rv.data

    login(client, app.config['USERNAME'],
            app.config['PASSWORD'])
    @pytest.fixture
    def test_user_post(self, client):
        """The method creates a user through an api"""

        with app.test_request_context():
            response = client.post(url_for('create_user'), data={
                'id': 1,
                'username': 'asheuh',
                'email': 'asheuh@gmail.com',
                'password': '1223456778'
            })
        assert b'asheuh' in response.data
        assert b'asheuh@gmail.com' in response.data
        assert b'1223456778' in response.data

    login(client, app.config['USERNAME'],
            app.config['PASSWORD'])
    def test_users_get(self, client):
        """The api test to see if it can get all users """
        with app.test_request_context():
            response = client.get(url_for('get_users'))
        assert response.status_code == 200

    login(client, app.config['USERNAME'],
            app.config['PASSWORD'])
    @pytest.fixture
    def test_user_put(self, client, user_id):
        """Api can perform update using PUT request """
        # data to be updated
        with app.test_request_context():
            response = client.put(url_for('get_users', user_id=1), data = {
                'username': 'mermaid',
                'email': 'paulla@gmail.com',
                'password': 'q0qq0q0q0qq0'
            })
        assert response.status_code == 200

    login(client, app.config['USERNAME'],
            app.config['PASSWORD'])
    @pytest.fixture
    def test_user_get(self, client, user_id):
        """This method tells the api to get a single user"""
        with app.test_request_context():
            response = client.get(url_for('get_one_user', user_id=1))
        assert response.status_code == 200
        assert response.json == self.user

    login(client, app.config['USERNAME'],
            app.config['PASSWORD'])
    @pytest.fixture
    def test_user_delete(self, client, user_id):
        """The api can delete a user"""
        with app.test_request_context():
            response = client.delete(url_for('delete_user', user_id=1))
        assert response.status_code == 200

    login(client, app.config['USERNAME'],
            app.config['PASSWORD'])
    @pytest.fixture
    def test_create_request(self, client):
        """The user can create a request"""
        with app.test_request_context():
            response = client.post(url_for('create_request'), data=dict(
                requestname="Internet connection",
                description="poor Internet connection on vpn",
                posted_date='1/21/2018'
            ), follow_redirects=True)
            
        assert b'Internet connection' in response.data
        assert b'poor Internet connection on vpn' in response.data
        assert b'1/21/2018' in response.data

    login(client, app.config['USERNAME'],
            app.config['PASSWORD'])
    def test_get_requests(self, client):

        """The user can get and view all the requests with (GET request"""
        with app.test_request_context():
            response = client.get(url_for('get_requests'))
        assert response.status_code == 200

    login(client, app.config['USERNAME'],
            app.config['PASSWORD'])
    @pytest.fixture
    def test_request_by_id_get(self, client, request_id):
        """The user can get a single request and view it (with GET request)"""
        with app.test_request_context():
            response = client.get(url_for('get_one_request', request_id=1))
        assert response.status_code == 200

    login(client, app.config['USERNAME'],
            app.config['PASSWORD'])
    @pytest.fixture
    def test_request_put(self, client, request_id):
        """The user can update a request with PUT request"""
        with app.test_request_context():
            response = client.put(url_for('update_request', request_id=1), data=dict(
            requestname="Malware",
            description="Hacked",
            posted_date='12/28/2018'
        ), follow_redirects=True)

        assert response.status_code == 200

    login(client, app.config['USERNAME'],
            app.config['PASSWORD'])
    @pytest.fixture
    def test_request_delete(self, client, request_id):
        """The user an delete a request"""
        with app.test_request_context():
            response = client.delete(url_for('delete_request', request_id=1))
        assert response.status_code == 200