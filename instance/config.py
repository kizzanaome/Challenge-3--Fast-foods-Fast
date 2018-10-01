class BaseConfig:
    
    DATABASE_URL = 'postgresql://postgres:1460@localhost:5433/fast_food_db'
    DEBUG= True


class DevelopmentConfig(BaseConfig):
    DEBUG = True

class TestingConfig(BaseConfig):
    DATABASE_URL = 'postgresql://postgres:1460@localhost:5433/testing_db'
    DEBUG = True
    

class ProductionConfig(BaseConfig):
    Debug =False

app_config={
    "development":DevelopmentConfig,
    "production":ProductionConfig,
    "testing":TestingConfig
    
}