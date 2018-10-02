from app import create_app
from app.database  import Database
import os
config_name = ""

if config_name == 'production':
     DATABASE_URL = 'postgres://cnvubaunffnlsa:2639efa048a47a8de9efa076d2912fe6a7de075896b82ef48971bf4f799830b4@ec2-54-221-225-11.compute-1.amazonaws.com:5432/d35aprkl2ds50e'
config_name = 'development'

app = create_app(config_name)

db = Database('postgresql://postgres:1460@localhost:5432/fast_food_db')

if __name__ == '__main__':
    db.create_tables()
    # db.drop_table('users','orders','food_items')
    app.run()

