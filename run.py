from app import create_app
from app.database  import Database

app = create_app('development')
db = Database('postgresql://postgres:1460@localhost:5433/fast_food_db')


if __name__ == '__main__':
    db.create_tables()
    # db.drop_table('users','orders','food_items')
    app.run()

