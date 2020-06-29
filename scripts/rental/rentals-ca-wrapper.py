import csv
import requests
import json
import numpy
import os.path
from os import path

# constants
UNIVERSITY = 'university'
ID = 'id'
RENTALS_CA_URL = 'https://rentals.ca/phoenix/api/v1.0.1/listings'
FAKE_USER_AGENT_HEADER = {
    'User-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36'}

# rentals.ca parameter key constants
LIMIT = 'limit'
MAP_COORDINATES = 'bbox'
TYPES = 'types'
DETAILS = 'details'

# rentals.ca response JSON attribtues mapper
BEDS_MIN_MAX = 'beds_range'
BATHS_MIN_MAX = 'baths_range'
COORDINATE = 'location'
PROPERTY_TYPE = 'property_type'
RENT_MIN_MAX = 'rent_range'
LAST_UPDATED = 'updated'
SUPPRESS_PAGINATION = 'suppress-pagination'

DEFAULT_PARAMS = {
    LIMIT: 500,
    DETAILS: 'mid1',
    # without suppress, returns only 10 listings
    SUPPRESS_PAGINATION: 1
}


class RentalsWrapper:
    @staticmethod
    def get_listings(json):
        return json['data']['listings']

# Calculate mean with outliers removed.


def calculate_mean(prices):
    prices = numpy.array(prices)
    mean = numpy.mean(prices)
    std_dev = numpy.std(prices)
    distance_from_mean = abs(prices - mean)
    max_deviations = 1.5
    not_outlier = distance_from_mean < max_deviations * std_dev
    no_outliers = prices[not_outlier]

    return numpy.mean(no_outliers)

# make restcall or load from cache


def get_listings(university, coordinate_list):
    rentals_map = None

    # considering university.json as a cache and not make REST call again.
    if path.exists("scripts/rental/cache/" + university + ".json"):
        print(f"Getting {university} file from cache")
        with open("scripts/rental/cache/" + university + ".json") as f:
            rentals_map = json.load(f)
    else:
        print(f"Getting {university} file from rentals.ca")
        rentals_map = request_listings(coordinate_list)
        # generate cache
        with open('scripts/rental/cache/' + university + '.json', 'w') as outfile:
            json.dump(rentals_map, outfile)
        print(f"Retrieved {len(rentals_map)} rentals from rentals.ca")

    return rentals_map


def request_listings(coordinate_list):
    params = dict(DEFAULT_PARAMS)
    params[MAP_COORDINATES] = ','.join(coordinate_list)

    rentals_res = requests.get(
        RENTALS_CA_URL,
        params=params,
        headers=FAKE_USER_AGENT_HEADER
    ).json()

    # 3. check meta data & check if region needs to be broken down into smaller quadrants

    total_properties = rentals_res['meta']['total_properties']
    returned_properties = rentals_res['meta']['returned_properties']

    if total_properties > returned_properties:
        print('breaking coordinates due to excessive listings')
        rentals_map = {}
        sliced_coordniates = get_sub_coordinates(coordinate_list)
        for coordinates in sliced_coordniates:
            rentals_map.update(request_listings(coordinates))
        return rentals_map
    else:
        return rental_json_to_map(rentals_res)


def get_sub_coordinates(coordinate_list):
    lon = {
        min: coordinate_list[0],
        max: coordinate_list[2],
    }
    lat = {
        min: coordinate_list[1],
        max: coordinate_list[3]
    }
    lon.mid = lon.max - lon.max
    lat.mid = lat.max - lat.max

    return [
        [lon.min, lat.min, lon.mid, lat.mid],
        [lon.mid, lat.min, lon.max, lat.mid],
        [lon.min, lat.mid, lon.mid, lat.max],
        [lon.mid, lat.mid, lon.max, lat.max],
    ]


def rental_json_to_map(json):
    rentals_map = {}
    listings = RentalsWrapper.get_listings(json)
    for listing in listings:
        rentals_map[listing[ID]] = listing
    return rentals_map


def scrape_rentals_api():
    # Map column title to column number
    field_dict = {}

    # 1. Iterate over csv & create GET API calls
    universities_query_csv = open('scripts/rental/query/university.csv')
    res_csv = open('scripts/rental/data/university.csv', 'w')

    print('Reading university csv file and result file')
    query_csv_reader = csv.reader(universities_query_csv)
    result_csv_writer = csv.writer(res_csv)
    average_rentals_dict = {} 

    for row in query_csv_reader:
        print('\n')
        if (query_csv_reader.line_num == 1):
            for i in range(len(row)):
                field_dict[row[i]] = i
            result_csv_writer.writerow(row)
            continue

        # 2. Make REST GET call to rentals.ca

        university = row[field_dict[UNIVERSITY]]
        rentals_map = get_listings(
            university,
            row[field_dict['min_long']:field_dict['max_lat'] + 1]
        )

        # TODO: compare above 2 and break down into smaller quadrant.

        listings = list(rentals_map.values())

        # Filter out properties with no rent_range
        listings = [listing for listing in listings if len(
            listing[RENT_MIN_MAX]) > 0]

        # Filter out properties with no beds_range
        listings = [listing for listing in listings if len(
            listing[BEDS_MIN_MAX]) > 0]

        # Get average price per room
        prices = []

        for listing in listings:
            rent_price = numpy.max(listing[RENT_MIN_MAX])
            room_count = numpy.max(listing[BEDS_MIN_MAX])

            # bachelors room
            if room_count < 1:
                room_count = 1

            prices.append(rent_price / room_count)

        row.append(calculate_mean(prices), len(rentals_map))

        result_csv_writer.writerow(row)


if __name__ == "__main__":
    scrape_rentals_api()
