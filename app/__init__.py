from flask import Flask, render_template, jsonify
from instance.config import app_config
from flask_restplus import Api
import os
from flask_cors import CORS


def create_app(config_name):
    app = Flask(__name__,instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    env = os.getenv('FLASK_ENV')

    api = Api(app, prefix='/api/v2', version='2.0',
            title='fsf', description='food delivery api')
        
    """swagger UI configurations"""
    app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    app.config.SWAGGER_UI_OPERATION_ID = True
    app.config.SWAGGER_UI_REQUEST_DURATION = True

    """We add JWT secret key constant"""
    app.config["JWT_SECRET_KEY"] = "k-i-z-z-a-n-a-o-m-e"

    """we import the JWTManager class from flask-jwt-extended library"""
    from flask_jwt_extended import JWTManager

    """   
     initialize jwt by passing our app instance to JWTManager class.

    """   
    jwt = JWTManager(app)

    """
    Registering blueprints

    """

    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from .orders import orders as orders_blueprint
    app.register_blueprint(orders_blueprint)

    from .food_items import food_items as food_items_blueprint 
    app.register_blueprint(food_items_blueprint)


    @app.errorhandler(405)
    def url_not_found(error):
        return jsonify({'message':'requested url is invalid'}), 405

    @app.errorhandler(404)
    def content_not_found(error):
        return jsonify({'message':'requested url is not found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'message':'internal server error'}), 500

    @app.errorhandler(500)
    def duplicate_keys(error):
        return jsonify({'message':'internal server error'}), 500


    @app.route('/')
    def index():
        return "Fast_food_fast_application"
    return app

    
