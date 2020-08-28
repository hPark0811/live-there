from models import *
from flask import Blueprint
from flask import request
from api.exception.exception_handler import *
import numpy as np
import pickle
import pgeocode
import os


# CONST
ML_MODEL_PATH = os.path.join('api', '_predictive', 'rental_rf')
PROPERTY_ALIAS_MAP = {
    'condo': ['apartment', 'condo'],
    'house': ['house', 'loft', 'duplex', 'multi-unit'],
    'town house': ['town house'],
    'bachelor': ['bachelor', 'studio']
}

# Config
rental_api = Blueprint('rental_api', __name__)
db = SQLAlchemy()

# Init Schema
rental_schema = RentalSchema()
rentals_schema = RentalSchema(many=True)


# Get all Rentals
@rental_api.route('', methods=['GET'])
def get_rentals():
    all_rentals = Rental.query.all()
    return rentals_schema.jsonify(all_rentals)


# Return predicted rental price.
@rental_api.route('/predict', methods=['GET'])
def predict_rental():
    valid_args = [
        request.args.get('universityId') is not None,
        request.args.get('bathCount') is not None,
        request.args.get('bedCount') is not None,
        request.args.get('propertyType') is not None, 
        request.args.get('postalCode') is not None
    ]

    if not all(valid_args):
        raise BadRequest('Must provide valid arguments')

    # Retrieve county.
    nomi = pgeocode.Nominatim('ca')
    postal_code = nomi.query_postal_code([request.args.get('postalCode')]).to_dict('records')[0]
    county = postal_code['county_name']

    # Load model.
    with open(os.path.join(ML_MODEL_PATH, 'model.pkl'), 'rb') as f:
        rf_model = pickle.load(f) 

    # Load scalers. 
    # TODO: only single one hot enocoding.
    with open(os.path.join(ML_MODEL_PATH, 'property_one_hot.pkl'), 'rb') as f:
        property_one_hot = pickle.load(f)

    with open(os.path.join(ML_MODEL_PATH, 'county_one_hot.pkl'), 'rb') as f:
        county_one_hot = pickle.load(f)

    with open(os.path.join(ML_MODEL_PATH, 'normalization.pkl'), 'rb') as f:
        scaler = pickle.load(f)

    # Average all the alias
    alias = PROPERTY_ALIAS_MAP[request.args.get('propertyType')]
    predictions = []

    # For each property type in alias, predict using RF model.
    for p in alias:
        # Normalize features.
        features = scaler.transform(np.array([int(request.args.get('bathCount')), int(request.args.get('bedCount'))]).reshape(1, -1))

        # One hot encode property and location.
        p_sparse = property_one_hot.transform(np.array([p]).reshape(1, -1)).toarray()
        c_sparse = county_one_hot.transform(np.array([county]).reshape(1, -1)).toarray()

        x = np.concatenate([features, p_sparse, c_sparse], axis=1)

        # Predict.
        predictions.append(rf_model.predict(x).item())

    return {
        'prediction': np.mean(predictions)
    }


@rental_api.route('/average', methods=['GET'])
def get_average_rental():
    if not request.args.get('universityId'):
        raise BadRequest('University ID must not be null')
    # default parameters
    min_distance_km = 0
    max_distance_km = 10
    property_types = None
    bed_count = 0
    bath_count = 0

    # TODO: Filter out edge cases
    if request.args.get('minDistance'):
        min_distance_km = request.args['minDistance']
    if request.args.get('maxDistance'):
        max_distance_km = request.args['maxDistance']
    if request.args.get('propertyType'):
        property_types = PROPERTY_ALIAS_MAP[
            request.args.get('propertyType')
        ]
    if request.args.get('bathCount'):
        bath_count = request.args.get('bathCount')
    if request.args.get('bedCount'):
        bed_count = request.args.get('bedCount')

    # Querying DB
    queried_rentals = db.session.query(
        Rental.rentalPrice,
        Rental.bathroomCount,
        Rental.bedroomCount,
        Rental.propertyType
    ).join(
        RentalRange,
        Rental.id == RentalRange.rentalId
    ).filter(
        RentalRange.universityId == request.args['universityId']
    ).filter(
        RentalRange.rentToUniversityDistance >= min_distance_km
    ).filter(
        RentalRange.rentToUniversityDistance <= max_distance_km
    )

    if property_types:
        queried_rentals = queried_rentals.filter(
            Rental.propertyType.in_(property_types))
    if bath_count:
        queried_rentals = queried_rentals.filter(
            Rental.bathroomCount == bath_count)
    if bed_count:
        queried_rentals = queried_rentals.filter(
            Rental.bedroomCount == bed_count)

    queried_rentals = queried_rentals.all()

    # Calculating average average
    rentals_count = len(queried_rentals)
    rentals_average = calculate_average_rent_per_room(queried_rentals)

    return {
        'rentalsCount': rentals_count,
        'average': rentals_average,
        'distance': max_distance_km
    }


def calculate_average_rent_per_room(rents):
    """ calculates average price of rent per room

    Args:
        rents (array[Rental])

    Returns:
        float: average price of rents per room
    """
    rent_prices_per_room = []
    for rent in rents:
        bedroom_count = rent.bedroomCount
        if bedroom_count == 0:
            bedroom_count = 1
        price_per_room = rent.rentalPrice / bedroom_count
        rent_prices_per_room.append(price_per_room)
    return calculate_mean(rent_prices_per_room)


def calculate_mean(nums):
    """ calculates mean with outliers removed

    Args:
        nums (array[int]): array of nums integers

    Returns:
        float: mean of nums
    """
    nums = np.array(nums)
    mean = np.mean(nums)
    std_dev = np.std(nums)
    distance_from_mean = abs(nums - mean)
    max_deviations = 1.5
    not_outlier = distance_from_mean < max_deviations * std_dev
    no_outliers = nums[not_outlier]

    return np.mean(no_outliers)