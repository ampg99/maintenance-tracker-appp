import unittest
"""
Importing unittest moduke
"""
import json
from run import create_app
from resources.users import UserResource

USERS = [
    {
        'id': 1,
        'username': 'brian',
        'email': 'brian@gmail.com',
        'password': '123456789'
    },
    {
        'id': 2,
        'username': 'paulla',
        'email': 'paulla@gmail.com',
        'password': '123456789'
    }
]
class User(unittest.TestCase):
    """
    This i a class for the test case of user
    """
    def setUp(self):
        """
        The method does the initialization of variables for test case
        """
        self.app = create_app(filename="config")
        self.client = self.app.test_client
        self.user = [user for user in USERS]
        for self.i in range(len(self.user)):
            return self.i

        self.new_user = {
            'username': 'sella',
            'email': 'sella@gmail.com',
            'password': '45464748'
        }



    def test_create_user(self):
        """
        The method creates a user through an api
        """
        response = self.client().post('/api/v1/users/', data=self.new_user)
        self.assertEqual(response.status_code, 201)


    def test_get_all_users(self):
        """
        The api test to see if it can get all users
        """
        response = self.client().get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        """
        Api can perform update using PUT request
        """
        # data to be posted
        data = {
            'username': 'avril',
            'email': 'avril@gmail.com',
            'password': 'avril'
        }
        # posts the data
        response = self.client().post('/api/v1/users/', data)
        self.assertEqual(response.status_code, 201)
        # data to be updated
        response = self.client().put('/api/v1/user/1', data = {
            'username': 'mermaid',
            'email': 'paulla@gmail.com',
            'password': 'q0qq0q0q0qq0'
        })
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):
        """
        This method tells the api to get a single user
        """
        response = self.client().get('/api/v1/users/<int:id>/', self.user[self.i]['id'])
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        """
        The api can delete a user
        """
        response = self.client().delete('api/v1/user/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
