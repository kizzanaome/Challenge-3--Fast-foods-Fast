import os
class BaseConfig:

    DATABASE_URL = 'postgresql://postgres:1460@localhost:5432/fast_food_db'
    DEBUG = True
    DB = 'fast_food_db'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DB = 'fast_food_db'

class TestingConfig(BaseConfig):
    if os.getenv('TRAVIS'):
        DATABASE_URL = 'postgres://postgres@localhost/testing_db'
    else:
        DATABASE_URL = 'postgres://postgres:1460@localhost:5432/testing_db'
    DEBUG = False
    Testing = True
    DB = 'testing_db'

class ProductionConfig(BaseConfig):
    os.getenv('FLASK_ENV')
    Debug = False
    DATABASE_URL = 'postgres://cnvubaunffnlsa:2639efa048a47a8de9efa076d2912fe6a7de075896b82ef48971bf4f799830b4@ec2-54-221-225-11.compute-1.amazonaws.com:5432/d35aprkl2ds50e'

app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig

}
