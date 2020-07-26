from models import *
from flask import Blueprint

rental_api = Blueprint('rental_api', __name__)

# Init Schema
rental_schema = RentalSchema()
rentals_schema = RentalSchema(many=True)

# Get all Rentals
@rental_api.route('', methods=['GET'])
def get_rentals():
    all_rentals = Rental.query.all()
    return rentals_schema.jsonify(all_rentals)
