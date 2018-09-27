"""This model handles databse related staff"""
from urllib.parse import urlparse
import psycopg2
from werkzeug.security import generate_password_hash
from flask import current_app as app
import psycopg2.extras as naome


class Database:
    """This class connects to the database"""

    def __init__(self, database_url):
        parsed_url = urlparse(database_url)
        db = parsed_url.path[1:]
        username = parsed_url.username
        hostname = parsed_url.hostname
        password = parsed_url.password
        port = parsed_url.port

        self.conn = psycopg2.connect(
            database=db, user= username, password= password,
            host =hostname, port=port
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor(cursor_factory=naome.RealDictCursor)

    def create_tables(self):
        """method for creating all tables"""
        commands =(
            """CREATE TABLE IF NOT EXISTS users(
                user_id SERIAL PRIMARY KEY,
                username varchar NOT NULL,
                password varchar NOT NULL,
                is_admin BOOLEAN NOT NULL
            )""",

            """CREATE TABLE IF NOT EXISTS food_items(
                food_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                food_name varchar NOT NULL,
                price INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE)""",

            """CREATE TABLE IF NOT EXISTS orders(
                order_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                food_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                location varchar NOT NULL,
                status varchar NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (food_id) REFERENCES food_items(food_id) ON DELETE CASCADE ON UPDATE CASCADE)"""    
        )

        for command in commands:
            print('tables created succesfully')
            self.cur.execute(command)
  
    def fetch_all_users(self):
        """ Fetches all user records from the database"""
        try:                  
            Sql = ("SELECT * FROM users;") 
            self.cur.execute(Sql)   
            rows = self.cur.fetchall()                 
            return rows         
        except (Exception, psycopg2.DatabaseError)as Error:
            raise Error

    def insert_user_data(self,username, password):
        try:
            sql = "INSERT INTO users (username,password) VALUES( %s,%s)"
            data = (username,password)   
            self.cur.execute(sql,data)
            return {'message':'user registered succesfully'},201
        except Exception as e:
            raise e
            # return {'msg':"Username Alrady exists{}".format(e)}

    def fetch_user(self, username):
        try:
            query = "SELECT * FROM users WHERE username=%s"
            self.cur.execute(query, (username,))
            user = self.cur.fetchone()
            username =user['username']
            password = user['password']
            print(username,password)
            return username, password
        except Exception as e:
            return {'msg': 'user not found'}, 404
        

    def drop_table(self, *table_names):
        ''' Drops the tables created '''
        for table_name in table_names:
            drop_table = "DROP TABLE IF EXISTS {} CASCADE".format(table_name)
            print('all tables dropped')
            self.cur.execute(drop_table)
