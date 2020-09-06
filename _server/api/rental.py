from models import *
from util import make_cache_key
from flask import Blueprint, request
from api.exception.exception_handler import *
import numpy as np
import pickle
import pgeocode
import os
from itertools import product


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

# Init Schema
rental_schema = RentalSchema()
rentals_schema = RentalSchema(many=True)

# Get all Rentals
@rental_api.route('', methods=['GET'])
@cache.cached(timeout=86400, key_prefix=make_cache_key)
def get_rentals():
    all_rentals = Rental.query.all()
    return rentals_schema.jsonify(all_rentals)


@rental_api.route('/average', methods=['GET'])
@cache.cached(timeout=86400, key_prefix=make_cache_key)
def get_rental_average():
    """ Return rental average.

    Args:
        universityId: university Id. If none -> raise BadRequest.
        postalCode: postal code used to get locational data from pgeocode. If none -> raise BadRequest. 
        maxDistance: radius of outer range. (default 15)
        minDistance: radius of inner range. (default 0)
        bedCount: number of bedroom.
            if not provided, 
                average metric: does not filter based on bedroom count.
                prediction metric: (weighted in future) average of predictions over bedCounts [1, 2, 3, 4, 5].
        bathCount: number of bedroom.
            if not provided, 
                average metric: does not filter based on bathroom count.
                prediction metric: (weighted in future) average of predictions over bathCounts [1, 2, 3, 4, 5].
        propertyType: type of the property.
            if not provided,
                average metric: does not filter based on propertyType.
    Returns:
        rentalCounts:
            average: number of rents that were used to calculate average.
            prediction: -1
        metrics: average(filter based) or prediction(random forest). (default average)
        average: average/prediction of rental prices.
            If there is no rentals data -> prediction based on random forest.
            If there is no rentals and propertyType is not provided, -1.       
        distance: maxDistance.
    """
    # TODO: Break this function to parts.

    # Check for invalid arguments.
    invalid_args = [
        request.args.get('universityId') is None,
        request.args.get('postalCode') is None
    ]

    if any(invalid_args):
        raise BadRequest('Must provide universityId and postalCode')

    """ Filter based average starts here by default. """

    # Default min/max distance.
    min_distance = 0
    max_distance = 15

    if request.args.get('minDistance'):
        min_distance = int(request.args.get('minDistance'))

    if request.args.get('maxDistnace'):
        max_distance = int(request.args.get('maxDistance'))

    # Querying DB & filter based on min/max radius and universityId.
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
        RentalRange.rentToUniversityDistance >= min_distance
    ).filter(
        RentalRange.rentToUniversityDistance <= max_distance
    )

    # Filter based on propertyType, bathCount, bedCount. If none, automatically unfiltered.
    if request.args.get('propertyType') is not None:
        queried_rentals = queried_rentals.filter(
            Rental.propertyType.in_(
                PROPERTY_ALIAS_MAP[request.args.get('propertyType')])
        )
    if request.args.get('bathCount') is not None:
        queried_rentals = queried_rentals.filter(
            Rental.bathroomCount == request.args.get('bathCount')
        )
    if request.args.get('bedCount') is not None:
        queried_rentals = queried_rentals.filter(
            Rental.bedroomCount == request.args.get('bedCount')
        )

    queried_rentals = queried_rentals.all()

    # Calculating average.
    rentals_count = len(queried_rentals)

    if rentals_count > 0:
        rentals_average = calculate_average_rent_per_room(queried_rentals)
        # Successfully calculated filtered average.
        return {
            'rentalsCount': int(rentals_count),
            'average': float(rentals_average),
            'distance': int(max_distance),
            'metric': 'average'
        }

    # Check if prediction is available.
    prd_valid = [
        request.args.get('propertyType') is not None,
        # request.args.get('bedCount') is not None,
        # request.args.get('bathCount') is not None
    ]

    """ Prediction starts here """
    if all(prd_valid):
        # Retrieve county from pgeocode.
        nomi = pgeocode.Nominatim('ca')
        location_data = nomi.query_postal_code(
            [request.args.get('postalCode')]).to_dict('records')[0]
        county = location_data['county_name']

        """ Load pickles. """
        with open(os.path.join(ML_MODEL_PATH, 'model.pkl'), 'rb') as f:
            rf_model = pickle.load(f)

        # TODO: only single one hot enocoding.
        with open(os.path.join(ML_MODEL_PATH, 'property_one_hot.pkl'), 'rb') as f:
            property_one_hot = pickle.load(f)

        with open(os.path.join(ML_MODEL_PATH, 'county_one_hot.pkl'), 'rb') as f:
            county_one_hot = pickle.load(f)

        with open(os.path.join(ML_MODEL_PATH, 'normalization.pkl'), 'rb') as f:
            scaler = pickle.load(f)

        # Average all the alias, bedRanges, bathRanges.
        alias = PROPERTY_ALIAS_MAP[request.args.get('propertyType')]
        bedRange = [1, 2, 3, 4, 5]
        bathRange = [1, 2, 3]

        if request.args.get('bedCount') is not None:
            bedRange = [int(request.args.get('bedCount'))]

        if request.args.get('bathCount') is not None:
            bathRange = [int(request.args.get('bathCount'))]

        predictions = []
        aggregator = product(alias, bedRange, bathRange)

        for p, bedCount, bathCount in aggregator:
            # Normalize features.
            features = scaler.transform(
                np.array([bathCount, bedCount]).reshape(1, -1))

            # One hot encode property and location.
            p_sparse = property_one_hot.transform(
                np.array([p]).reshape(1, -1)).toarray()
            c_sparse = county_one_hot.transform(
                np.array([county]).reshape(1, -1)).toarray()

            x = np.concatenate([features, p_sparse, c_sparse], axis=1)

            # Predict.
            predictions.append(rf_model.predict(x).item())

        # TODO: Instead of average <- mean(predictions) must be weighted average based on probability distribution for each alias, bathRange, bedCount.
        if request.args.get('bedCount') is None:
            # Considering all of bedCounts have probability distribution.
            pdf = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
            divisor = np.dot(pdf, np.array(bedRange))
        else:
            divisor = float(request.args.get('bedCount'))

        # Successfully calculated rental predictions.
        return {
            'rentalsCount': -1,
            'average':  np.mean(predictions)/divisor,
            'distance': -1,
            'metric': 'prediction'
        }
    else:
        # Unavaiable to provide meaningful average.
        return {
            'rentalsCount': 0,
            'average': -1,
            'distance': int(max_distance),
            'metric': 'average'
        }


def calculate_average_rent_per_room(rents):
    # TODO: accounts for NaN values, and fix format.
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
    # TODO: accounts for NaN values, and fix format.
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
