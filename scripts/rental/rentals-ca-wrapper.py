import csv
import requests
import json
import numpy
import os.path
from os import path

# Calculate mean with outliers removed.
def calculate_mean(prices):
  prices = numpy.array(prices)
  mean = numpy.mean(prices)
  std_dev = numpy.std(prices)
  distance_from_mean = abs(prices - mean)
  max_deviations = 2
  not_outlier = distance_from_mean < max_deviations * std_dev
  no_outliers = prices[not_outlier]

  return numpy.mean(no_outliers)

# constants
UNIVERSITY = 'university'
RENTALS_CA_URL = 'https://rentals.ca/phoenix/api/v1.0.1/listings'
FAKE_USER_AGENT_HEADER = {'User-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36'}

# rentals.ca parameter key constants
CITY = 'obj_path'
LIMIT = 'limit'
MAP_COORDINATES = 'bbox'
TYPES = 'types'
DEATILS = 'details'

# rentals.ca response JSON attribtues mapper
BEDS_MIN_MAX = 'beds_range'
BATHS_MIN_MAX = 'baths_range'
COORDINATE = 'location'
PROPERTY_TYPE = 'property_type'
RENT_MIN_MAX = 'rent_range'
LAST_UPDATED = 'updated'
SUPPRESS_PAGINATION = 'suppress-pagination'

default_params = {
  LIMIT: 500,
  DEATILS: 'mid1',
  # without suppress, returns only 10 listings
  SUPPRESS_PAGINATION: 1
}

# Map column title to column number
field_dict = {}

# 1. Iterate over csv & create GET API calls
cities_query_file = open('scripts/rental/query/cities.csv')
average_rentals_json = open('scripts/rental/data/res.json', 'r')

cities_csv = csv.reader(cities_query_file)
average_rentals_dict = json.load(average_rentals_json)

for row in cities_csv:
  if (cities_csv.line_num == 1):
    for i in range(len(row)):
      field_dict[row[i]] = i
    continue
  
  # 2. Make REST GET call to rentals.ca

  city = row[field_dict[CITY]]
  rentals_res = None

  # considering city.json as a cache and not make REST call again.
  if path.exists("scripts/rental/data/" + city + ".json"):
    with open("scripts/rental/data/" + city + ".json") as f:
      rentals_res = json.load(f)
  else:
    params = dict(default_params)
    
    params[MAP_COORDINATES] = ','.join(row[field_dict['min_long']:field_dict['max_lat'] + 1])

    rentals_res = requests.get(
        RENTALS_CA_URL,
        params=params,
        headers=FAKE_USER_AGENT_HEADER
      ).json()
    # generate cache
    with open('scripts/rental/data/' + city + '.json', 'w') as outfile:
      json.dump(rentals_res, outfile)

  # 3. check meta data & check if region needs to be broken down into smaller quadrants

  total_properties = rentals_res['meta']['total_properties']
  returned_properties = rentals_res['meta']['returned_properties']
  # TODO: compare above 2 and break down into smaller quadrant.

  listings = rentals_res['data']['listings']

  # Filter out properties with no rent_range
  listings = [listing for listing in listings if len(listing[RENT_MIN_MAX]) > 0]

  # Filter out properties with no beds_range
  listings = [listing for listing in listings if len(listing[BEDS_MIN_MAX]) > 0]

  # Get average price per room 
  prices = []

  for listing in listings:
    rent_price = numpy.max(listing[RENT_MIN_MAX])
    room_count = numpy.max(listing[BEDS_MIN_MAX])

    # bachelors room
    if room_count < 1:
      room_count = 1

    prices.append(rent_price / room_count)

  average_price_per_room = calculate_mean(prices)
  average_rentals_dict[city] = average_price_per_room

# create average rentals data
with open('scripts/rental/data/res.json', 'w') as res:  
  json.dump(average_rentals_dict, res)
