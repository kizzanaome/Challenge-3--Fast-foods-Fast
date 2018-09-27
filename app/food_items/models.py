from app.database import Database
from flask import current_app as app
import psycopg2.extras as naome
import psycopg2

"""
    Global variable food_items  holds  foods , initially its empty
"""
class Food(Database):
    def __init__(self, user_id,food_name,price):
        """
            This method acts as a constructor
            for our class, its used to initialise class attributes
        """
        self.user_id= user_id
        self.food_name = food_name
        self.price = price
        Database.__init__(self,app.config['DATABASE_URL'])


    def create_foodItems(self):
        """
            This method receives an object of the
            class, creates and returns a dictionary from the object
        """
        
        try:
            sql = "INSERT INTO food_items (user_id,food_name,price) VALUES(%s,%s,%s)"
            data = (self.user_id,self.food_name,self.price) 
            food=self.cur.execute(sql,data)  
            print(food)
            return {'message':'food_item has succesfully been placed succesfully'},201
        except Exception as e:
            raise e

    # def fetch_food_item(self):
    #     query ="SELECT FROM food_items WHERE food_id =%s"
    #     self.cur.execute(query, (self.food_id,))
    #     food = self.cur.fetchone() 
    #     fd= food[self.food_id]
    #     return fd

    def fetch_all_food_items(self):
        """ Fetches all food_items records from the database"""
        try:                  
            Sql = ("SELECT * FROM food_items;") 
            self.cur.execute(Sql)   
            rows = self.cur.fetchall()                 
            return rows         
        except (Exception, psycopg2.DatabaseError)as Error:
            raise Error

    # def single_order(self, order_id):
    #     query= "SELECT * FROM orders WHERE order_id = '{}'".format(order_id)
    #     self.cur.execute(query)
    #     oder=self.cur.fetchone()
    #     return oder
                

