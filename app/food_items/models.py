from app.database import Database
from flask import current_app as app
import psycopg2.extras as naome
import psycopg2


"""
    Global variable db holds the db instance
"""

class Food():
    def __init__(self, user_id,food_name,price):
        """
            This method acts as a constructor
            for our class, its used to initialise class attributes
        """
        self.user_id= user_id
        self.food_name = food_name
        self.price = price
        

    def create_foodItems(self):
        """
            This method inserts data into the food_items tables
        """    
        db = Database(app.config['DATABASE_URL'])

        try:
            sql = "INSERT INTO food_items (user_id,food_name,price) VALUES(%s,%s,%s)"
            data = (self.user_id,self.food_name,self.price) 
            food=db.cur.execute(sql,data)  
            print(food)
            return {'message':'food_item has succesfully been placed succesfully'},201
        except Exception as e:
            raise e

    def check_food_name(self, food_name):
        db = Database(app.config['DATABASE_URL'])

        query = "SELECT * FROM food_items WHERE food_name=%s"
        db.cur.execute(query, (food_name,))
        user = db.cur.fetchone()
        print(user)
        if user:
            return True
        return False

    
    @staticmethod
    def fetch_all_food_items():
        """ Fetches all food_items records from the database"""
        db = Database(app.config['DATABASE_URL'])

        try:                  
            Sql = ("SELECT * FROM food_items where food_id=%s;") 
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
            Sql = ("SELECT * FROM food_items") 
            db.cur.execute(Sql)   
            rows = db.cur.fetchall()  
            print(rows)               
            return rows         
        except (Exception, psycopg2.DatabaseError)as Error:
            raise Error

    @staticmethod
    def delete_food_items(food_id):
        db = Database(app.config['DATABASE_URL'])
        query = "DELETE FROM food_items WHERE food_id='{}' ".format(food_id)
        db.cur.execute(query, (food_id),)
      