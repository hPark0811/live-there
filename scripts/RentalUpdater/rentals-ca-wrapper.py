import csv
import os

import requests
import numpy
import pgeocode
import mysql.connector
import dateutil.parser
import time

# constants
UNIVERSITY = 'universityName'
CAMPUS = 'campus'
POSTAL_CODE = 'postalCode'
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

DB = mysql.connector.connect(
    host="35.225.74.52",
    user="root",
    password="livethere2020",
    database="livethere"
)

INSERT_SQL = """
INSERT IGNORE INTO livethere.Rental
(`rentalPrice`,
`postalCode`,
`longitude`,
`latitude`,
`stubId`,
`bathroomCount`,
`bedroomCount`,
`lastUpdatedDate`)
VALUES
(%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s);
"""

CURSOR = DB.cursor()

NOMI = pgeocode.Nominatim('ca')


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


def generate_coordinate_range(lon, lat, range_in_km):
    distance_metic = range_in_km / 111
    min_long = lon - distance_metic
    min_lat = lat - distance_metic
    max_long = lon + distance_metic
    max_lat = lat + distance_metic
    return [
        min_long,
        min_lat,
        max_long,
        max_lat
    ]


# make rest call or load from cache


def fetch_listings(university, postal_code):
    rentals_map = None
    if len(postal_code) == 6:
        postal_code = postal_code[:3] + ' ' + postal_code[3:]
    location_data = NOMI.query_postal_code(postal_code).to_dict()
    coordinate_list = generate_coordinate_range(
        location_data['longitude'],
        location_data['latitude'],
        10 #km
    )

    print(f"Getting {university} rentals from rentals.ca")
    rentals_map = request_listings(coordinate_list)
    print(f"Retrieved {len(rentals_map)} rentals from rentals.ca")

    return rentals_map


def request_listings(coordinate_list):
    params = dict(DEFAULT_PARAMS)
    params[MAP_COORDINATES] = ','.join(map(str, coordinate_list))

    rentals_res = requests.get(
        RENTALS_CA_URL,
        params=params,
        headers=FAKE_USER_AGENT_HEADER
    ).json()

    time.sleep(2)

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
    lon_min = coordinate_list[0]
    lon_max = coordinate_list[2]
    lat_min = coordinate_list[1]
    lat_max = coordinate_list[3]

    lon_mid = lon_min + (lon_max - lon_min) / 2
    lat_mid = lat_min + (lat_max - lat_min) / 2

    return [
        [lon_min, lat_min, lon_mid, lat_mid],
        [lon_mid, lat_min, lon_max, lat_mid],
        [lon_min, lat_mid, lon_mid, lat_max],
        [lon_mid, lat_mid, lon_max, lat_max],
    ]


def rental_json_to_map(json):
    rentals_map = {}
    listings = RentalsWrapper.get_listings(json)
    for listing in listings:
        rentals_map[listing[ID]] = listing
    return rentals_map


def listing_to_insert_value(listing):
    return (
        numpy.max(listing[RENT_MIN_MAX]),
        str(listing['postal_code']).replace(" ", ""),
        listing['location']['lng'],
        listing['location']['lat'],
        listing['id'],
        numpy.max(listing['baths_range']),
        numpy.max(listing[BEDS_MIN_MAX]),
        dateutil.parser.parse(listing['updated']).strftime('%Y-%m-%d')
    )


def scrape_rentals_api():
    # Map column title to column number
    field_dict = {}

    # 1. Iterate over csv & create GET API calls
    # TODO: Get these from DB directly
    universities_csv_path = os.path.join(os.path.dirname(__file__), 'query', 'universities.csv')
    universities_query_csv = open(universities_csv_path)

    print('Reading university csv file and result file')
    query_csv_reader = csv.reader(universities_query_csv)

    for row in query_csv_reader:
        print('\n')
        if query_csv_reader.line_num == 1:
            for i in range(len(row)):
                field_dict[row[i]] = i
            continue

        # 2. Make REST GET call to rentals.ca

        rentals_map = fetch_listings(
            row[field_dict[UNIVERSITY]],
            row[field_dict[POSTAL_CODE]]
        )

        listings = list(rentals_map.values())

        # Filter out properties with no rent_range
        listings = [listing for listing in listings if len(
            listing[RENT_MIN_MAX]) > 0]

        # Filter out properties with no beds_range
        listings = [listing for listing in listings if len(
            listing[BEDS_MIN_MAX]) > 0]

        listings_to_insert = list(map(
            lambda listing: listing_to_insert_value(listing),
            listings
        ))

        print('executing update')
        CURSOR.executemany(INSERT_SQL, listings_to_insert)
        DB.commit()


if __name__ == "__main__":
    scrape_rentals_api()
