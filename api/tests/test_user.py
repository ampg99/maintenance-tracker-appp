import unittest
import json
from run import create_app
from resources.users import RequestsListResource, RequestResource

"""
Importing unittest moduke
"""

class UserTestCase(unittest.TestCase):
    """
    This i a class for the test case of user
    """
    def setUp(self):
        """
        The method does the initialization of variables for test case
        """
        self.app = create_app(filename="config")
        self.client = self.app.test_client()
        self.user = {
            'id': 1,
            'username': 'asheuh',
            'email': 'asheuh@gmail.com',
            'password': '1223456778'
        }

    def login(self, *args, **kwargs):
        """
        This method logs in the user
        """
        return self.client.post('/api/v1/login', data=dict(**kwargs), follow_redirects=True)

    def logout(self, *args):
        """
        This method logs out the user and redirects them to a page
        """
        return self.client.get('/api/v1/logout', follow_redirects=True)

    def test_create_user(self):
        """
        The method creates a user through an api
        """
        response = self.client.post('/api/v1/users/', data=self.user)
        self.assertEqual(response.status_code, 201)


    def test_get_users(self):
        """
        The api test to see if it can get all users
        """
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        """
        Api can perform update using PUT request
        """
        # data to be updated
        response = self.client.put('/api/v1/user/1', data = {
            'username': 'mermaid',
            'email': 'paulla@gmail.com',
            'password': 'q0qq0q0q0qq0'
        })
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):
        """
        This method tells the api to get a single user
        """
        response = self.client.get('/api/v1/users/<int:id>/')
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        """
        The api can delete a user
        """
        response = self.client.delete('/api/v1/user/1')
        self.assertEqual(response.status_code, 200)

    def test_user_create_request(self):
        """
        The user can create a request
        """
        self.login(self, 'asheuh@gmail.com', '2927374747')
        response = self.client.post('/api/v1/requests/', data=dict(
            Id="1",
            request_name="Internet connection",
            description="poor Internet connection on vpn",
            posted_date='1/21/2018'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 201)

    def test_get_request(self):
        """
        The user can get and view all the requests with (GET request)
        """
        self.login(self, 'asheuh', '2827374938')
        response = self.client.get('/api/v1/requests/')
        self.assertEqual(response.status_code, 200)

    def test_get_request_by_id(self):
        """
        The user can get a single request and view it (with GET request)
        """
        self.login(self, 'paulla@gmail.com', '12345678')
        response = self.client.get('/api/v1/requests/1/')
        self.assertEqual(response.status_code, 200)

    def test_update_request(self):
        """
        The user can update a request with PUT request
        """
        self.login(self, 'paulla@gmail.com', '12345678')
        response = self.client.put('/api/v1/requests/1/', data=dict(
            request_name="Malware",
            description="Hacked",
            posted_date='12/28/2018'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    def test_delete_request(self):
        """
        The user can delete a request
        """
        self.login(self, 'paulla@gmail.com', '12345678')
        response = self.client.delete('/api/v1/requests/1')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """
        The method test user log in with correct input
        """
        response = self.login(self, 'paulla@gmail.com', '12345678')
        self.assertIn('The page title', response.data)
        # Tests for Invalid user email input
        response = self.login(self, 'paulla@gmail.com' + 't', '12345678')
        self.assertIn('Invalid email address', response.data)
        # Test for invalid user password input
        response = self.login(self, 'paulla@gmail.com', '12345678' + 't')
        self.assertIn('Invalid password given', response.data)

    def test_logout(self):

        """
        The method test user log out and tells the user if they are logged out
        and then redirects them to a page
        """
        response = self.logout(self)
        self.assertIn('You are now logged out', response.data)

    def tearDown(self):
        super(UserTestCase, self).tearDown()
        pass

if __name__ == '__main__':
    unittest.main()
