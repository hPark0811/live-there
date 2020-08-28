#Business Search      URL -- 'https://api.yelp.com/v3/businesses/search'
#Business Match       URL -- 'https://api.yelp.com/v3/businesses/matches'
#Phone Search         URL -- 'https://api.yelp.com/v3/businesses/search/phone'
#Business Details     URL -- 'https://api.yelp.com/v3/businesses/{id}'
#Business Reviews     URL -- 'https://api.yelp.com/v3/businesses/{id}/reviews'

#Businesses, Total, Region

# Import the modules
import requests
import json

# Define a business ID
business_id = '4AErMBEoNzbk7Q8g45kKaQ'
unix_time = 1546047836

# Define my API Key, My Endpoint, and My Header
API_KEY = 'Oi5-90HLHSBa-m9N_4lcLUiQpjpAVSyW-_QVe7sqRP8qmtIf1VZKYuq6ouIzpzE_4pB3hUjqQAPAXLnD9mEiVx9M8J1aJH23zE6qBMzcEa8l4wITJh7aQk61L2k_X3Yx'
#ENDPOINT = 'https://api.yelp.com/v3/businesses/{}/reviews'.format(business_id)
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
#ENDPOINT = 'https://api.yelp.com/v3/businesses/gy5pr5bFAjOL5rERSdMCLg'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

# Define my parameters of the search
# BUSINESS SEARCH PARAMETERS - EXAMPLE
PARAMETERS = {'term': 'restaurants, All',
              'limit': 50,
              'offset': 51,
            #   'radius': 10000,
              'categories': 'bars',
              'location': 'University of Toronto'}

# BUSINESS MATCH PARAMETERS - EXAMPLE
#PARAMETERS = {'name': 'Peets Coffee & Tea',
#              'address1': '7845 Highland Village Pl',
#              'city': 'San Diego',
#              'state': 'CA',
#              'country': 'US'}

# Make a request to the Yelp API
response = requests.get(url = ENDPOINT,
                        params = PARAMETERS,
                        headers = HEADERS)

# Conver the JSON String
business_data = response.json()


with open('/Users/saminouralla/Desktop/restaurantData.json', 'w', encoding='utf-8') as f:
    json.dump(business_data, f, ensure_ascii=False, indent=3)

with open('/Users/saminouralla/Desktop/restaurantData.json', 'r') as JSON:
       json_dict = json.load(JSON)


with open('/Users/saminouralla/Desktop/filteredData.json', 'w', encoding='utf-8') as f:
    json.dump(json_dict, f, ensure_ascii=False, indent=1)