from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from .models import User
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
from app.database import Database
from flask import current_app as app
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_claims)


class Register(Resource):
    def get(self):
        try:
            # db = Database(app.config['DATABASE_URL'])
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
            parser.add_argument('is_admin')
            args = parser.parse_args()

            password = generate_password_hash(
                args['password'], method='sha256')

            """creating an insatnce of a user class"""
            use = User('username', 'password', is_admin=False)
            create_user = use.insert_user_data(
                args['username'], password, args['is_admin'])
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

        """read from database to find the user and then check the password"""

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
            return {'message': 'I nvalid credentials'}, 401
