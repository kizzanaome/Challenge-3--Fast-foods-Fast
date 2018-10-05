from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from .models import  Food
from flask import request
import psycopg2
from app.database import Database
from flask import current_app as app
from app.decorator import admin_only
import re
import string
from flask_jwt_extended import jwt_required,get_jwt_identity


class FoodItems(Resource):
    @jwt_required
    def get(self):
        """ methods gets all food_items"""
        try:
            fd=Food.fetch_food_name_and_price()
            if not fd:
                return {"msg": " There are no food_items at the momnet"}, 200 
            return make_response(jsonify({"Food_Menu": fd}),200)
            
        except (Exception, psycopg2.DatabaseError)as Error:
            print(Error)
   
    @jwt_required
    @admin_only
    def post(self):
        """ defining the request parser and expected arguments in the request"""
        current_user = get_jwt_identity()
        parser= reqparse.RequestParser()
        parser.add_argument("food_name",
                            type=str,
                            required=True,
                            help="The food_name field can't be empty")
        parser.add_argument("price",
                            type=int,
                            required=True,
                            help="Price cant be coverted ")
        args = parser.parse_args()

        if not args['food_name']:
            return make_response(jsonify({"message": "Add food_name"}),400)       
        if args['price'] == "":
            return make_response(jsonify({"message":"Add price"}),400) 
        if ' ' in args['food_name']:
            return {'message': 'Please avoid adding spaces before characters'}, 400
        if not re.compile('^[a-zA-Z]+$').match(args['food_name']):
            return {'message': 'foodname should be in characters'}, 400
            
        if len(str(args['food_name'])) < 4:
            return {'message': 'food_name should be more than 4 characters'}, 400

        """creating an insatnce of a food_items class"""
        chars = string.whitespace + string.punctuation + string.digits
        food = Food(current_user,args["food_name"].strip(chars), args["price"])
        food_name_exist= food.check_food_name(args['food_name'].strip(chars))
        if food_name_exist:
            return {'message': 'Food item has alreadly beeen placed'}, 403
        create_food=food.create_foodItems()
        if create_food:
            return make_response(jsonify({'massege':"you have succesfully placed a food_item"}),201)
        return {"msg": "food_item not placed succesfully"}, 400






     
        