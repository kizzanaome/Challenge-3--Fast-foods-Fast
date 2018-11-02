from app.database import Database
from flask import current_app as app
from werkzeug.security import generate_password_hash
import psycopg2.extras as naome
from flask_restplus import Api
import psycopg2


class User():    
    """This class handles database transactions for the user"""
    def __init__(self, username,password, is_admin=False):
        self.username = username
        self.password=password
        self.is_admin= is_admin
        

    def insert_user_data(self,username, password, is_admin):
        try:
            db = Database(app.config['DATABASE_URL'])

            sql = "INSERT INTO users (username,password,is_admin) VALUES(%s, %s,%s)"
            data = (username,password, is_admin)   
            user=db.cur.execute(sql,data)
            print(user)
            return {'message':'user registered succesfully'},201
        except Exception as e:
            raise e

    def insert_user_admin(self,username, password,is_admin):
        try:
            db = Database(app.config['DATABASE_URL'])

            sql = "INSERT INTO users (username,password, is_admin) VALUES( %s,%s,%s)"
            data = (username,password,is_admin)   
            user=db.cur.execute(sql,data)
            print(user)
            return {'message':'user registered succesfully'},201
        except Exception as e:
            raise e
                        
    def fetch_user(self, username):  
        db = Database(app.config['DATABASE_URL'])

        query = "SELECT * FROM users WHERE username=%s"
        db.cur.execute(query, (username,))
        user = db.cur.fetchone()
        print(user)
        return user
    
    def check_user(self, username):
        db = Database(app.config['DATABASE_URL'])

        query = "SELECT * FROM users WHERE username=%s"
        db.cur.execute(query, (username,))
        user = db.cur.fetchone()
        if user:
            return True
        return False

    def fetch_all_users(self):
        """ Fetches all user records from the database"""
        try:                
            db = Database(app.config['DATABASE_URL'])
  
            Sql = ("SELECT * FROM users;") 
            db.cur.execute(Sql)   
            rows = db.cur.fetchall() 
            print(rows)                
            return rows         
        except (Exception, psycopg2.DatabaseError)as Error:
            raise Error

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
        
    
