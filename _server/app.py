from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

#routes import
from api import rental, university
from models import *
import config

# Init app
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

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
