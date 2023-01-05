from flask import Flask
from product_routes import product_route
from db import db
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    db_uri = os.environ['SQLALCHEMY_DB_URI']
    app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI=db_uri,    
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
 
    app.register_blueprint(product_route)

    db.app = app

    db.init_app(app)
    return app