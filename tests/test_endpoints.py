import unittest
from app import create_app
from flask import current_app as app
import json
from app.orders.models import Order
from app.database import Database


class BaseCase(unittest.TestCase):
    """class holds all the unittests for the app"""

    def setUp(self):
        """
            This method is run at the beginig of each test
            also initialises the client where tests will be run

        """
        
        config_name = 'testing'
        self.app = create_app(config_name)
        self.app_context = self.app.app_context()

        self.app_context.push()
        self.db = Database(app.config['DATABASE_URL'])
        self.db.create_tables()
        self.client = self.app.test_client()

        self.user = {
            'username': 'bbb',
            'password': 'naome'

        }

    def test_user_resgestration(self):
        response = self.client.post(
            'api/v1/auth/signup', data=json.dumps(self.user), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('you have succesfully signed up', str(response.data))

    def test_user_login(self):
        response = self.client.post(
            'api/v1/auth/signup', data=json.dumps(self.user), content_type='application/json')

        response = self.client.post(
            'api/v1/auth/login', data=json.dumps(self.user), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('User succesfully confimed',str(response.data))

    def tearDown(self):
        print('------Tearingdown----------------------')
        self.db.drop_table('users','orders','food_items')
