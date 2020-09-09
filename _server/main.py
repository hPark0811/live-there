"""
    TODO: All server relevent files should be stored in app/* as python package & main folder must call app.py from app package.
    TODO: Recommended backend server structure
        _server:
            deployment config files.
            main.py (or run.py) - run app.py & gcloud calls app.py/app(flask app). & contain options for dev/deployment
            app:
                app config files.
                app.py
                api:
                    __init__.py
                    api related files
                ml:
                    __init__.py
                    pickles folder
                models.py
                utils.py
"""

from flask import Flask, request, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from api import rental, university, utility, restaurant
from api.exception.exception_handler import *
from models import db, cache
from models import *

import os
import config


def create_app():
    # Init app
    app = Flask(__name__)

    CORS(app)
    basedir = os.path.abspath(os.path.dirname(__file__))

    # DB Config
    app.config.from_object('config.SqlAlchemyConfig')

    # Init db
    db.init_app(app)

    # Init cache

    app.config['CACHE_TYPE'] = 'simple'
    cache.init_app(app)

    # Init routes
    app.register_blueprint(rental.rental_api, url_prefix='/rental')
    app.register_blueprint(university.university_api, url_prefix='/university')
    app.register_blueprint(utility.utility_api, url_prefix='/utility')
    app.register_blueprint(restaurant.restaurant_api, url_prefix='/restaurant')

    @app.route("/")
    def root():
        return 'LiveThere Microservice is Running!'

    # Generic Exception handler
    @app.errorhandler(GenericException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        return response

    return app

app = create_app()

# Run Server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
