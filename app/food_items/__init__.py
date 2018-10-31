from flask import Blueprint
from flask_restful import Api
from .views import FoodItems

food_items = Blueprint('food', __name__, url_prefix='/api/v1')

food_api = Api(food_items)

food_api.add_resource(FoodItems, '/menu')