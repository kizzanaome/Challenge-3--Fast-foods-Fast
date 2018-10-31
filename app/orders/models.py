from app.database import Database
from flask import current_app as app
import psycopg2.extras as naome
import psycopg2




class Order:
    """ Class for modeling orders """

    def __init__(self, user_id, food_id, quantity, location, status):
        """
            This method acts as a constructor
            for our class, its used to initialise class attributes
        """
        self.user_id = user_id
        self.food_id = food_id
        self.quantity = quantity
        self.location = location
        self.status = status

    def insert_order_data(self):
        """
            This method inserts data into the orders tables
        """          
        try:
            db = Database(app.config['DATABASE_URL'])

            sql = "INSERT INTO orders (user_id,food_id,quantity,location,status) VALUES(%s,%s,%s,%s,%s)"
            data = (self.user_id, self.food_id,
                    self.quantity, self.location, self.status)
            order = db.cur.execute(sql, data)
            print(order)
            return {'message': 'order  placed succesfully'}, 201
        except Exception as e:
            raise e
    
    def single_order(self, order_id):
        db = Database(app.config['DATABASE_URL'])

        query = """SELECT  od.quantity, od.status, od.location, od.CREATED_AT,od.order_id,usr.username,
                     f.price, f.food_name from orders 
                     as od JOIN food_items as f ON od.food_id=f.food_id JOIN 
                     users as usr ON  od.user_id=usr.user_id where order_id ='{}'""".format(order_id)
        db.cur.execute(query, (order_id))
        oder = db.cur.fetchone()
        print(oder)
        return oder


    @staticmethod
    def fetch_all_orders():
        db = Database(app.config['DATABASE_URL'])

        """ Fetches all order records from the database"""
        try:
            Sql = """SELECT  od.quantity, od.status, od.location, od.CREATED_AT, od.order_id,
                     f.price, f.food_name, usr.username from orders as od JOIN food_items 
                     as f ON od.food_id=f.food_id JOIN users as usr ON  od.user_id=usr.user_id;"""
            db.cur.execute(Sql)
            rows = db.cur.fetchall()
            return rows
        except (Exception, psycopg2.DatabaseError)as Error:
            raise Error

    @staticmethod
    def order_history(user_id):
        db = Database(app.config['DATABASE_URL'])

        Sql = """SELECT  od.order_id, od.quantity, od.status,od.location,od.CREATED_AT,
                    f.price, f.food_name, usr.username from orders 
                    as od JOIN food_items as f ON od.food_id=f.food_id JOIN
                    users as usr ON od.user_id=usr.user_id where od.user_id ='{}' """.format(user_id)
        db.cur.execute(Sql)
        rows = db.cur.fetchall()
        return rows

   
    @staticmethod
    def fetch_single_food_id(food_id,):
        db = Database(app.config['DATABASE_URL'])

        query = "SELECT * FROM food_items WHERE food_id ='{}'".format(food_id)
        db.cur.execute(query, (food_id),)
        fooditem = db.cur.fetchone()
        return fooditem

    @staticmethod
    def fetch_user_by_id(user_id):
        try:
            db = Database(app.config['DATABASE_URL'])

            query = "SELECT * FROM users WHERE user_id=%s"
            db.cur.execute(query, (user_id,))
            user = db.cur.fetchone()
            print(user)
            return user
        except Exception as e:
            return {'msg': 'user not found'}, 404

    @staticmethod
    def fetch_foodname(food_name):
        db = Database(app.config['DATABASE_URL'])

        query = "SELECT * FROM food_items WHERE food_name=%s"
        db.cur.execute(query, (food_name,))
        food = db.cur.fetchone()
        return food

    @staticmethod
    def update_status(status, order_id):
        db = Database(app.config['DATABASE_URL'])

        query = """UPDATE orders
                SET status = %s
                WHERE order_id = %s"""
        db.cur.execute(query, (status, order_id))
        updated_rows = db.cur.rowcount
        print(updated_rows)
        return updated_rows

    @staticmethod
    def fetch_food_id(food_id, user_id):

        db = Database(app.config['DATABASE_URL'])

        query = "SELECT * FROM orders WHERE food_id=%s and user_id=%s"
        db.cur.execute(query, (food_id,user_id))
        orders = db.cur.fetchone()
        return orders

