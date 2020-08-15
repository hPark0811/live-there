from models import *
from flask import Blueprint
from flask import request
import numpy
from api.exception.exception_handler import *

restaurant_api = Blueprint('restaurant_api', __name__)
db = SQLAlchemy()

# Init Schema
restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)

# Get all Restaurants


@restaurant_api.route('', methods=['GET'])
def get_restaurants():
    all_restaurants = Restaurant.query.all()
    return restaurant_schema.jsonify(all_restaurants)


@restaurant_api.route('/averageRestaurantPrice', methods=['GET'])
def get_average_restaurantPrice():
    if not request.args.get('universityId'):
        raise BadRequest('University ID must not be null')
    # default parameters
    min_distance_km = 0
    max_distance_km = 10
    restaurant__type = None
    

    # TODO: Filter out edge cases
    if request.args.get('minDistance'):
        min_distance_km = request.args['minDistance']
    if request.args.get('maxDistance'):
        max_distance_km = request.args['maxDistance']
    if request.args.get('restaurantTypes'):
        restaurantTypes = property_type_alias_mapper(
            request.args.get('restaurantTypes')
        )
    

    # Querying DB
    queried_restaurants = db.session.query(
        Restaurant.yelpId,
        Restaurant.restaurantType
    ).join(
        RestaurantRange,
        Restaurant.restaurantId == RestaurantRange.restaurantId
    ).join(
        YelpSchema,
        Restaurant.yelpId == YelpSchema.yelpId
    ).filter(
        RestaurantRange.universityId == request.args['universityId']
    ).filter(
        RestaurantRange.restaurantToUniversityDistance >= min_distance_km
    ).filter(
        RestaurantRange.restaurantToUniversityDistance <= max_distance_km
    )

    queried_restaurants = queried_restaurants.all()

    # Calculating average average
    restaurants_count = len(queried_restaurants)
    dineIn_Average=calculate_average_dineIn(queried_restaurants)
    bar_Average=calculate_average_Bar(queried_restaurants)


    return {
        'Dine In Average': dineIn_Average,
        'Bar Average': bar_Average,
        'Number of Restaurants and Bars':restaurants_count
    }

def calculate_average_Bar(stores):
   
    restaurantPrices = []
    for store in stores:
        if store.restaurantType == 'B':
            priceRange = store.priceLevel
            restaurantPrices.append(priceRange)
    return calculate_mean(restaurantPrices)


def calculate_average_dineIn(stores):
   
    restaurantPrices = []
    for store in stores:
        if store.restaurantType == 'D':
            priceRange = store.priceLevel
            restaurantPrices.append(priceRange)
    return calculate_mean(restaurantPrices)



def calculate_mean(nums):
    
    nums = numpy.array(nums)
    mean = numpy.mean(nums)
    std_dev = numpy.std(nums)
    distance_from_mean = abs(nums - mean)
    max_deviations = 1.5
    not_outlier = distance_from_mean < max_deviations * std_dev
    no_outliers = nums[not_outlier]

    return numpy.mean(no_outliers)


def restaurant_type_alias_mapper(alias):
  

    if (alias == 'restaurant'):
        return ['D']
    if (alias == 'bar'):
        return ['B']
    
    # TODO: Handle unmapped alias error
    return None
