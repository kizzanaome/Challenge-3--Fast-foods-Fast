import unittest
from app import create_app
from flask import current_app as app
import json
from app.database import Database
from .test_data import *

class BaseCase(unittest.TestCase):
    """class holds all the unittests for the endpoints"""

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
        

    def create_valid_user(self):
            """ Registers a user to be used for tests"""
            response = self.client.post('/api/v1/auth/asignup',
                                        data=json.dumps(user),
                                        content_type='application/json')
            return response
    
    def get_token(self):
        ''' Generates a toke to be used for tests'''
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(user),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        return'Bearer '+ data['token']

    def post_menu(self):

        """method for posting a menu """
        response = self.client.post(
            'api/v1/menu', data=json.dumps(menu), content_type='application/json', headers={'Authorization':
                                             self.get_token()})
        return response

    def place_an_order(self):

        """method for posting a menu """
        response = self.client.post(
            'api/v1/users/orders', data=json.dumps(order), content_type='application/json', headers={'Authorization':
                                             self.get_token()})
        return response


    def test_user_resgistration(self):
        response = self.create_valid_user()
        self.assertEqual(response.status_code, 201)
        self.assertIn('you have succesfully signed up', str(response.data))    


    # def test_user_for_existing_user(self):
    #     response = self.create_valid_user()
    #     response = self.create_valid_user()
    #     self.assertEqual(response.status_code, 403)
    #     # self.assertIn('you have succesfully signed up', str(response.data))

    def test_invalid_signup_input(self):
        """method for  testing post a an order  endpoint"""

        response = self.client.post(
            'api/v1/auth/asignup', data=json.dumps(invalid_user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Username field is required"', str(response.data))
    
    def test_invalid_login_input(self):
        """method for posting a an order """

        response = self.client.post(
            'api/v1/auth/login', data=json.dumps(invalid_user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Username field is required"', str(response.data))


    # def test_admin_registration(self):
    #     """method for testing an admin signup"""
    #     response = self.client.post(
    #         'api/v1/auth/asignup', data=json.dumps(user), content_type='application/json')
    #     self.assertEqual(response.status_code, 201)
    #     self.assertIn('you have succesfully signed up', str(response.data))

     
    def test_user_login(self):
        """method for testing user_login endpoint"""
        self.create_valid_user()
        response = self.client.post(
            'api/v1/auth/login', data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print(response.data)
        data = json.loads(response.data.decode())
        self.assertTrue(data['token'])

    """
        This method tests for the fetch food_menu endpoint
    """
    def test_fetch_food_items(self):
        self.create_valid_user()
        response = self.client.get('api/v1/menu', content_type='application/json', headers={'Authorization':
                                             self.get_token()})
        self.assertEqual(response.status_code, 200)
    
    # def test_place_a_food_items(self):
    #     self.create_valid_user()
    #     response = self.client.post('api/v1/menu', data=json.dumps(menu), content_type='application/json',
    #                                 headers={'Authorization': self.get_token()})
    #     self.assertEqual(response.status_code, 201)
    #     self.assertIn('you have succesfully placed a food_item', str(response.data))

        
    # def test_fetch_a_single_order(self):
    #     self.create_valid_user()
    #     self.post_menu()
    #     self.place_an_order()
    #     response = self.client.get('api/v1/orders/1', data=json.dumps(order), content_type='application/json',
    #                                headers={'Authorization': self.get_token()})
    #     self.assertEqual(response.status_code, 200)
        

    # def test_update_order_status(self):
    #     self.create_valid_user()
    #     self.post_menu()
    #     self.place_an_order()
    #     response = self.client.put('api/v1/orders/1',
    #                                content_type='application/json', data=json.dumps(updated_status),
    #                                headers={'Authorization': self.get_token()})
    #     self.assertEqual(response.status_code, 201)
    #     self.assertIn("status updated succesfully", str(response.data))

    def test_get_order_history_doesnt_exist(self):
        self.create_valid_user()
        self.post_menu()
        self.place_an_order()
        response = self.client.get('api/v1/users/orders', content_type='application/json', 
                                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 200)


    def tearDown(self):
        """method for rearing down the tables whenever a test is completed"""
        print('------Tearingdown----------------------')
        self.db.drop_table('users','orders','food_items')
   