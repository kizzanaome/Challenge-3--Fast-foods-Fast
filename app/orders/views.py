from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from .models import  Order
from flask import request
import re
import string
import psycopg2
from app.database import Database
from flask import current_app as app
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.decorator import admin_only
import flasgger

class OrderList(Resource):
    @jwt_required
    def get(self):
            current_user = get_jwt_identity()
            orders=Order.order_history(current_user)
            print(orders)
            if not orders:
                return {"msg": "You have not orderd for any food so you have no order history"}, 200 
            return make_response(jsonify({"Your_order_History": orders}),200)  

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        print(current_user)
        """ Passing of incoming data inside post requests"""
        parser= reqparse.RequestParser(bundle_errors=True)

        """we add parameters to parse foodname, quantity and location"""
        parser.add_argument("food_name",
                            type=str,
                            required=True,
                            help="The food_name field cant be empty")        
        parser.add_argument("quantity",
                            type=int,
                            required=True,
                            help="The quantity field cant be empty")
        parser.add_argument("location", 
                            type=str,
                            required=True,
                            help="The location field cant be empty")
        args=parser.parse_args()

        if not args['food_name']:
            return {"message": "Add food_name"}, 400

        if args['location'] == "":
            return {"message": "Add location"},400
        if ' ' in args['food_name']:
                return {'message': 'Please avoid adding spaces'}, 400

        if ' ' in args['location']:
            return {'message': 'Please avoid adding spaces'}, 400

        if not re.compile('^[a-zA-Z]+$').match(args['food_name']):
            return {'message': 'food_name should be in characters'}, 400

        if not re.compile('^[a-zA-Z]+$').match(args['location']):
            return {'message': 'location should be in characters'}, 400
   
        if len(str(args['food_name'])) < 4:
            return {'message': 'food_name should be more than 4 characters'}, 400
        status = "pending"
        chars = string.whitespace + string.punctuation + string.digits
        food_name = args['food_name'].strip(chars)
        fd =Order.fetch_foodname(food_name)

        if fd:
            """creating an insatnce of an order class"""
            order = Order(current_user,fd['food_id'],args['quantity'], args['location'],status)
            select_order=order.fetch_food_id(fd['food_id'],current_user)   
            if select_order:
                    return {'message':'Order has already been placed'},400
            create_order=order.insert_order_data()
            if create_order:
                return {'message':"you have succesfully placed order"},201
            return {"msg": "Order not placed succesfully"}, 
        return {"msg": "food_item doesnt exist on the food menu"}, 404


class SingleOrder(Resource):
    @jwt_required
    @admin_only
    def get(self, order_id):        
        status = 'pending'  
        if order_id:
            ode = Order('user_id','food_id','quantity','location',status)
            oder = ode.single_order(order_id)
            if not oder:
                return {'msg': "order not found "},404
            return {"order": oder},200

    @jwt_required
    @admin_only
    def put(self,order_id):
        parser = reqparse.RequestParser()
        parser.add_argument('status')
        args = parser.parse_args()
        status = args['status']
        if not args['status']:
            return {"message":"Add status"},400

        if ' ' in args['status']:
            return {'message': 'Please avoid adding spaces'}, 400
        update_status = Order.update_status(status, order_id)
        if update_status:
            if status == 'Accepted':
                return {'message':'Order has been accepted'},201
            return {'message':'order has been Rejected'}, 201
        return {'message':'Failed to update status'},400
        

class AdminOrderView(Resource):
    @jwt_required
    @admin_only
    def get(self):
            orders=Order.fetch_all_orders()
            print(orders)
            if not orders:
                return {"msg": " There are no orders at the moment"}, 200 
            return make_response(jsonify({"Available_orders": orders}),200) 

   
     

            


     
