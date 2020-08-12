from models import *
from flask import Blueprint
from flask import request
import numpy
from api.exception.exception_handler import *

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
    if request.args.get('propertyTypes'):
        property_types = property_type_alias_mapper(
            request.args.get('propertyTypes')
        )
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
        queried_rentals = queried_rentals.filter(Rental.propertyType.in_(property_types))
    if bath_count:
        queried_rentals = queried_rentals.filter(Rental.bathroomCount == bath_count)
    if bed_count:
        queried_rentals = queried_rentals.filter(Rental.bedroomCount == bed_count)

    queried_rentals = queried_rentals.all()

    # Calculating average average
    rentals_count = len(queried_rentals)
    rentals_average = calculate_average_rent_per_room(queried_rentals)

    return {
        'rentals_count': rentals_count,
        'average': rentals_average
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
    nums = numpy.array(nums)
    mean = numpy.mean(nums)
    std_dev = numpy.std(nums)
    distance_from_mean = abs(nums - mean)
    max_deviations = 1.5
    not_outlier = distance_from_mean < max_deviations * std_dev
    no_outliers = nums[not_outlier]

    return numpy.mean(no_outliers)


def property_type_alias_mapper(alias):
    """ map property property alias names to existing property 
    types in the database

    Args:
        alias (string))
    """

    if (alias == 'condo'):
        return ['apartment', 'condo']
    if (alias == 'house'):
        return ['house', 'loft', 'duplex', 'multi-unit']
    if (alias == 'town house'):
        return ['town house']
    if (alias == 'bachelor'):
        return ['bachelor', 'studio']

    # TODO: Handle unmapped alias error
    return None
