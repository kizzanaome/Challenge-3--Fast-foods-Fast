from flask import jsonify, make_response
from flask_restplus import Resource, reqparse, fields, Api
from .models import User
import re
import string
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
from app.database import Database
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_claims)


class Register(Resource):
    def get(self):
        try:
            use = User('username', 'password')
            rows = use.fetch_all_users()
            if rows == True:
                return {"msg": " There are no users at the momnet"}, 200
            return make_response(jsonify({"users": rows}), 200)
        except (Exception, psycopg2.DatabaseError)as Error:
            print(Error)

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str,
                                required=True, help="This field is required")
            parser.add_argument('password')
            args = parser.parse_args()
            password = generate_password_hash(
                args['password'], method='sha256')
            if not args['username']:
                return make_response(jsonify({"message":"Username field is required"}), 400) 
            if re.compile('^[1234567890]+$').match(args['username']):
                return make_response(jsonify({"message":"This field is a string"}), 400) 
            if ' ' in args['username']:
                return {'message': 'Please avoid adding spaces before characters'}, 400

            if ' ' in args['password']:
                return {'message': 'Please avoid adding spaces before and after characters'}, 400

            if len(str(args['username'])) < 4:
                return {'message': 'username should be more than 4 characters'}, 400

            if len(str(args['password'])) < 4:
                return {'message': 'password should be more than 4 characters'}, 400

            """creating an insatnce of the user class"""
            chars = string.whitespace + string.punctuation + string.digits
            use = User(args['username'].strip(chars), args['password'], is_admin=False)
            username = args['username'].strip(chars)
            user = use.check_user(username)            
            if user:
                return {'message': 'Username already exists'}, 403
            use.insert_user_data(args['username'].strip(chars), password, is_admin=False)
            return make_response(jsonify({'message': "you have succesfully signed up"}), 201)
        except Exception as e:
            raise e


class AdminSignIn(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str,
                                required=True, help="This field is required")
            parser.add_argument('password')

            args = parser.parse_args()

            password = generate_password_hash(
                args['password'], method='sha256')
            
            if not args['username']:
                return make_response(jsonify({"message":
                                              "Username field is required"}),
                                     401)
            if not args['password']:
                return make_response(jsonify({"message":
                                              "Password field is required"}),
                                     401)
            if  ' ' in args['username']:
                return {'message': 'Please avoid adding spaces'}, 400

            if ' ' in args['password']:
                return {'message': 'Please avoid adding spaces'}, 400

            if re.compile('^[a-zA-Z]+$').match(args['username']):
                return {'message': 'Please dont input symbols'}, 400

            if len(str(args['username'])) < 4:
                return {'message': 'username should be more than 4 characters'}, 400

            if len(str(args['password'])) < 4:
                return {'message': 'password should be more than 4 characters'}, 400

            """creating an insatnce of a user class"""
            use = User(args['username'], args['password'], is_admin=True)
            user = use.check_user(args['username'])
            
            if user:
                return {'message': 'Username already exists'}, 403
            create_user = use.insert_user_admin(
                args['username'], password, is_admin=True)
            if create_user:
                return make_response(jsonify({'message': "you have succesfully signed up"}), 201)
        except Exception as e:
            raise e
            return {'massage': 'username already exists'}, 400


class Login(Resource):
    def post(self):
        """
        Allows users to login to their accounts

        """
        data = request.get_json()
        username = data['username']
        password = data['password']
        use = User('username', 'password')
        if not data['username']:
                return make_response(jsonify({"message":
                                              "Username field is required"}),
                                     401)
        if not data['password']:
            return make_response(jsonify({"message":
                                            "Password field is required"}),
                                    401)
        if ' ' in data['username']:
            return {'message': 'Please avoid adding spaces '}, 400

        if ' ' in  data['password']):
            return {'message': 'Please avoid adding spaces'}, 400

        if re.compile('^[a-zA-Z]+$').match(data['username']):
            return {'message': 'Please dont input symbols'}, 400

        if len(str(data['username'])) < 4:
            return {'message': 'username should be more than 4 characters'}, 400

        if len(str(data['password'])) < 4:
            return {'message': 'password should be more than 4 characters'}, 400

        """
            read from database to find the user and then check the password
        
        """

        user = use.fetch_user(username)
        print(user)
        if user and check_password_hash(user['password'], password):
            print(user)
            print(type(user))
            user_token = {}
            access_token = create_access_token(identity=user['user_id'])
            user_token["token"] = access_token
            return user_token, 200
        else:
            return {'message': 'Invalid credentials'}, 401
