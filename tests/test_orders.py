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

    """This methods tests for placing an order end point """
    def test_place_an_order(self):
        response = self.client.post(
            'api/v1/auth/asignup', data=json.dumps(user), content_type='application/json')
        response = self.client.post(
            'api/v1/auth/login', data=json.dumps(user), content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data['token'])
        response = self.client.post('api/v1/menu', data=json.dumps(menu), content_type='application/json',
                                    headers={'Authorization': 'Bearer {}'.format(data['token'])})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('api/v1/users/orders', data=json.dumps(order), content_type='application/json',
                                    headers={'Authorization': 'Bearer {}'.format(data['token'])})
        self.assertEqual(response.status_code, 201)
        self.assertIn('you have succesfully placed order', str(response.data))
        

    def test_get_order_history_doesnt_exist(self):
        response = self.client.post(
            'api/v1/auth/asignup', data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('you have succesfully signed up', str(response.data))
        response = self.client.post(
            'api/v1/auth/login', data=json.dumps(user), content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data['token'])
        response = self.client.post('api/v1/menu', data=json.dumps(menu), content_type='application/json',
                                    headers={'Authorization': 'Bearer {}'.format(data['token'])})
        response = self.client.post('api/v1/users/orders', data=json.dumps(order), content_type='application/json',
                                    headers={'Authorization': 'Bearer {}'.format(data['token'])})
        response = self.client.get('api/v1/menu', content_type='application/json', headers={
                                   'Authorization': 'Bearer {}'.format(data['token'])})
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """method for rearing down the tables whenever a test is completed"""
        print('------Tearingdown----------------------')
        self.db.drop_table('users','orders','food_items')

