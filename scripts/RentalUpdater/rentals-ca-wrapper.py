import requests
import numpy
import dateutil.parser
import time
from utility import geo, sql

# constants
NAME = 'universityName'
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


# make rest call or load from cache


def fetch_listings(university, postal_code):
    location_data = geo.ca_postal_code_to_location_data(postal_code)

    if isinstance(location_data['longitude'], float):
        coordinate_list = geo.generate_coordinate_range(
            location_data['longitude'],
            location_data['latitude'],
            20  # km
        )

        print(f"Getting {university} rentals from rentals.ca")
        return request_listings(coordinate_list)
    else:
        return {}


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
        dateutil.parser.parse(listing['updated']).strftime('%Y-%m-%d'),
        listing['property_type']
    )


def scrape_rentals_api():
    dbms = sql.RentalDBMS()

    # 1. Iterate over csv & create GET API calls
    # TODO: Get these from DB directly
    universities_df = dbms.get_all_universities()

    for universityNdx, university in universities_df.iterrows():
        print('initiating fetch for ' + university[NAME] + ' university\n')
        # 2. Make REST GET call to rentals.ca

        rentals_map = fetch_listings(
            university[NAME],
            university[POSTAL_CODE]
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
        dbms.cursor.executemany(sql.RENTAL_INSERT_SQL, listings_to_insert)
        dbms.commit()


if __name__ == "__main__":
    scrape_rentals_api()
