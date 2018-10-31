from app import create_app
from app.database  import Database
config_name = "production"
db = Database('postgres://diryjyzvjynvec:ccedd1fbfa7da622aa1da72b26fa2c117623172cd7df4f5090c0040bcba41244@ec2-107-20-211-10.compute-1.amazonaws.com:5432/d2gutubl34hhni')
app = create_app(config_name)

if __name__ == '__main__':
    db.create_tables()
    # db.drop_table('users','orders','food_items')
    app.run()
