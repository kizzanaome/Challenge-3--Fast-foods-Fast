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

    
    @staticmethod
    def fetch_all_food_items():
        """ Fetches all food_items records from the database"""
        db = Database(app.config['DATABASE_URL'])
        try:                  
            Sql = ("SELECT * FROM food_items;") 
            db.cur.execute(Sql)   
            rows = db.cur.fetchall()                 
            return rows         
        except (Exception, psycopg2.DatabaseError)as Error:
            raise Error

    @staticmethod
    def fetch_food_name_and_price():
        """ Fetches all food_items records from the database"""
        db = Database(app.config['DATABASE_URL'])
        try:                  
            Sql = ("SELECT  food_name, price FROM food_items") 
            db.cur.execute(Sql)   
            rows = db.cur.fetchall()  
            print(rows)               
            return rows         
        except (Exception, psycopg2.DatabaseError)as Error:
            raise Error



                

