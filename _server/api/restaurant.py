from models import *
from util import make_cache_key
from flask import Blueprint, request
import numpy
from api.exception.exception_handler import *

restaurant_api = Blueprint('restaurant_api', __name__)

# Init Schema
restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)

# Get all Restaurants


@restaurant_api.route('', methods=['GET'])
@cache.cached(timeout=86400, key_prefix=make_cache_key)
def get_restaurants():
    all_restaurants = Restaurant.query.all()
    return restaurant_schema.jsonify(all_restaurants)


@restaurant_api.route('/average', methods=['GET'])
@cache.cached(timeout=86400, key_prefix=make_cache_key)
def get_average_restaurantPrice():
    if not request.args.get('universityId'):
        raise BadRequest('University ID must not be null')
    # default parameters
    min_distance_km = 0
    max_distance_km = 10
    minReviews = 0
    selected_prices = None

    # TODO: Filter out edge cases
    if request.args.get('minDistance'):
        min_distance_km = request.args['minDistance']
    if request.args.get('maxDistance'):
        max_distance_km = request.args['maxDistance']

    if request.args.get('minReviews'):
        minReviews = request.args.get('minReviews')
    if request.args.get('selectedPrices'):
        selected_prices = request.args.get('selectedPrices').split(',')

    # Querying DB
    queried_restaurants = db.session.query(
        Restaurant.priceLevel,
        Restaurant.ratingCount,
        Restaurant.yelpId
    ).join(
        RestaurantRange,
        Restaurant.restaurantId == RestaurantRange.restaurantId
    ).filter(
        RestaurantRange.universityId == request.args['universityId']
    ).filter(
        RestaurantRange.restaurantToUniversityDistance >= min_distance_km
    ).filter(
        RestaurantRange.restaurantToUniversityDistance <= max_distance_km
    )

    if minReviews:
        queried_restaurants = queried_restaurants.filter(
            Restaurant.ratingCount >= minReviews)
    if selected_prices and not 'ALL' in selected_prices:
        queried_restaurants = queried_restaurants.filter(
            Restaurant.priceLevel.in_(selected_prices))
    queried_restaurants = queried_restaurants.all()

    # Calculating average average
    restaurants_count = len(queried_restaurants)
    dine_in_average = calculate_average_dineIn(queried_restaurants)

    return {
        'average': dine_in_average,
        'restaurantCount': restaurants_count
    }


""" def calculate_average_Bar(stores):
   
    restaurantPrices = []
    for store in stores:
        if store.restaurantType == 'B':
            priceRange = store.priceLevel
            restaurantPrices.append(priceRange)
    return calculate_mean(restaurantPrices) """


def calculate_average_dineIn(stores):

    restaurantPrices = []
    for store in stores:
        priceRange = store.priceLevel
        if priceRange == '$':
            priceRange = 10
        if priceRange == '$$':
            priceRange = 16
        if priceRange == '$$$':
            priceRange = 26
        if priceRange == '$$$$':
            priceRange = 40
        restaurantPrices.append(priceRange)
    return calculate_mean(restaurantPrices)


def calculate_mean(nums):

    nums = numpy.array(nums)
    mean = numpy.mean(nums)

    return mean


def restaurant_type_alias_mapper(alias):

    if (alias == 'restaurant'):
        return ['D']
    if (alias == 'bar'):
        return ['B']

    # TODO: Handle unmapped alias error
    return None
