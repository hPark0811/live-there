from flask import Flask, request, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

#routes import
from api import rental, university, utility, restaurant
from api.exception.exception_handler import *
from models import *
import config

# Init app
#app = Flask(__name__, static_folder="../_client/livethere-app/build/static", template_folder="../_client/livethere-app/build")
app = Flask(__name__)

CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# DB Config
app.config.from_object('config.SqlAlchemyConfig')

# Init db
db = SQLAlchemy(app)

# Init routes
app.register_blueprint(rental.rental_api, url_prefix='/rental')
app.register_blueprint(university.university_api, url_prefix='/university')
app.register_blueprint(utility.utility_api, url_prefix='/utility')
app.register_blueprint(restaurant.restaurant_api, url_prefix='/restaurant')

""" 
@app.route("/")
def root():
    return render_template('index.html') 
"""
@app.route("/")
def root():
    return 'LiveThere Microservice is Running!'

# Generic Exception handler
@app.errorhandler(GenericException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    return response

# Run Server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)