import unittest
from app import create_app
from flask import current_app as app
import json
from app.orders.models import Order
from app.database import Database
from .test_data import *


class BaseCase(unittest.TestCase):
    """class holds all the unittests for the app"""

    def setUp(self):
        """
            This method is run at the begining of each test
            also initialises the client where tests will be run

        """
        
        config_name = 'testing'
        self.app = create_app(config_name)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = Database(app.config['DATABASE_URL'])
        self.db.create_tables()
        self.client = self.app.test_client()


    def test_user_resgistration(self):
        response = self.client.post(
            'api/v1/auth/signup', data=json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('you have succesfully signed up', str(response.data))


    def test_admin_registration(self):

        """method for testing an admin signup"""
        response = self.client.post(
            'api/v1/auth/asignup', data=json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('you have succesfully signed up', str(response.data))

    def test_user_login(self):

        """method for testing user_login endpoint"""
        response = self.client.post(
            'api/v1/auth/signup', data=json.dumps(user), content_type='application/json')

        response = self.client.post(
            'api/v1/auth/login', data=json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue(data['token'])

    def tearDown(self):
        """method for rearing down the tables whenever a test is completed"""
        print('------Tearingdown----------------------')
        self.db.drop_table('users','orders','food_items')
