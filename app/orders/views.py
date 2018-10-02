from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from .models import  Order
from flask import request
import psycopg2
from app.database import Database
from flask import current_app as app
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.decorator import admin_only

class OrderList(Resource):
    @jwt_required
    def get(self):
            orders=Order.order_history()
            print(orders)
            if not orders:
                return {"msg": "You have not orderd for any food so you have no order history"}, 200 
            return make_response(jsonify({"Your order History": orders}),200)  

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
        status = "pending"
        food_name = args['food_name']
        fd =Order.fetch_foodname(food_name)
        print(fd)
        if fd:
            """creating an insatnce of an order class"""
            print(current_user)
            order = Order(current_user,fd['food_id'],args['quantity'], args['location'],status)
            select_order=order.fetch_food_id(fd['food_id'])   
            if select_order:
                    return {'message':'Order has already been placed'},403
            create_order=order.insert_order_data()
            if create_order:
                return make_response(jsonify({'massege':"you have succesfully placed order"}),201)
            return {"msg": "Order not placed succesfully"}, 
        return {"msg": "food_item doesnt exist on the food menu"}, 400


class SingleOrder(Resource):
    @jwt_required
    @admin_only
    def get(self, order_id):        
        status = 'pending'  
        if order_id:
            ode = Order('user_id','food_id','quantity','location',status)
            oder = ode.single_order(order_id)
            print (oder)
            if not oder:
                return {'msg': "order not found "},404
            return make_response(jsonify({"order": oder}),200)
            
    @jwt_required
    @admin_only
    def put(self,order_id):
        parser = reqparse.RequestParser()
        parser.add_argument('status')
        args = parser.parse_args()
        status = args['status']
        update_status= Order.update_status(status, order_id)
        if update_status:
            return {'message':'status updated succesfully'}, 201
        return {'message':'Failed to update status'},400

class AdminOrderView(Resource):
    @jwt_required
    @admin_only
    def get(self):
            orders=Order.fetch_all_orders()
            print(orders)
            if not orders:
                return {"msg": " There are no orders at the moment"}, 200 
            return make_response(jsonify({"Available_orders": orders}, ),200)  

   
     

            


     
