from flask import Blueprint
from flask_restful import Api
from .views import Register,Login, AdminSignIn

users = Blueprint('users', __name__, url_prefix='/api/v1')

users_Api = Api(users)

users_Api.add_resource(AdminSignIn, '/auth/asignup')
users_Api.add_resource(Register, '/auth/signup')
users_Api.add_resource(Login, '/auth/login')

