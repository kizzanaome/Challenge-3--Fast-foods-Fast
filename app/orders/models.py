from app.database import Database
from flask import current_app as app
import psycopg2.extras as naome
import psycopg2


class Order(Database):
    """ Class for modeling orders """

    def __init__(self, user_id, food_id,quantity, location, status):
        """
            This method acts as a constructor
            for our class, its used to initialise class attributes
        """
        self.user_id = user_id
        self.food_id = food_id
        self.quantity = quantity
        self.location = location
        self.status = status
        Database.__init__(self, app.config['DATABASE_URL'])

    def insert_order_data(self):
        try:
            sql = "INSERT INTO orders (user_id,food_id,quantity,location,status) VALUES(%s,%s,%s,%s,%s)"
            data = (self.user_id, self.food_id,
                    self.quantity, self.location, self.status)
            order = self.cur.execute(sql, data)
            print(order)
            return {'message': 'order  placed succesfully'}, 201
        except Exception as e:
            raise e

    @staticmethod
    def fetch_all_orders():
        """ Fetches all order records from the database"""
        db = Database(app.config['DATABASE_URL'])
        try:
            Sql = """SELECT od.order_id, od.quantity, od.status, od.location,
                     f.food_id, f.food_name from orders as od JOIN food_items as f ON od.food_id=f.food_id;"""   
            db.cur.execute(Sql)
            rows = db.cur.fetchall()
            return rows
        except (Exception, psycopg2.DatabaseError)as Error:
            raise Error

    @staticmethod
    def fetch_order_history():
        db = Database(app.config['DATABASE_URL'])
        Sql = """SELECT od.order_id, od.quantity, od.status, od.location,
                    f.food_id, f.food_name from orders as od JOIN food_items as f ON od.food_id=f.food_id;"""   
        db.cur.execute(Sql)
        rows = db.cur.fetchall()
        return rows


    def single_order(self, order_id):
        query = "SELECT * FROM orders WHERE order_id = '{}'".format(order_id)
        self.cur.execute(query)
        oder = self.cur.fetchone()
        return oder

    @staticmethod
    def fetch_single_food_id(food_id,):
        db = Database(app.config['DATABASE_URL'])
        query = "SELECT * FROM food_items WHERE food_id ='{}'".format(food_id)
        db.cur.execute(query, (food_id),)
        fooditem = db.cur.fetchone()
        return fooditem

    @staticmethod
    def fetch_foodname(food_name):
        db = Database(app.config['DATABASE_URL'])
        query = "SELECT * FROM food_items WHERE food_name=%s"
        db.cur.execute(query, (food_name,))
        food = db.cur.fetchone()
        return food

        # self.cur.execute(query, (username,))
        # user = self.cur.fetchone()
        # username =user['username']
        # password = user['password']
        # print(username,password)
        # return username, password
