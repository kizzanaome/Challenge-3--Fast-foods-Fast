import os
class BaseConfig:
    
    DATABASE_URL = 'postgresql://postgres:1460@localhost:5433/fast_food_db'
    DEBUG= True
    DB ='fast_food_db'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DB='fast_food_db'

class TestingConfig(BaseConfig):
    if os.getenv('TRAVIS'):
        DATABASE_URL='postgres://postgres@localhost/testing_db'
    else:
        DATABASE_URL = 'postgres://postgres:1460@localhost:5433/testing_db'
    DEBUG = False
    Testing =True
    DB = 'testing_db'

class ProductionConfig(BaseConfig):
    Debug =False

app_config={
    "development":DevelopmentConfig,
    "production":ProductionConfig,
    "testing":TestingConfig
    
}