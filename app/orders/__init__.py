from flask import Blueprint
from flask_restful import Api
from .views import OrderList,SingleOrder,AdminOrderView

orders = Blueprint('orders', __name__, url_prefix='/api/v1')

"""Imported Api class from flask_restfull to initialize the Api"""
"""We create an orders_api object and attach our app to it"""
orders_api = Api(orders)

""" Registering our endpoints inside the application"""
"""We add resources to corresponding endpoints """

orders_api.add_resource(OrderList, '/users/orders')
orders_api.add_resource(SingleOrder, '/orders/<int:order_id>')
orders_api.add_resource(AdminOrderView, '/orders')



