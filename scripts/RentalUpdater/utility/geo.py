import pgeocode

CA_NOMI = pgeocode.Nominatim('ca')


def generate_coordinate_range(lon, lat, range_in_km):
    distance_metric = range_in_km / 111
    min_long = lon - distance_metric
    min_lat = lat - distance_metric
    max_long = lon + distance_metric
    max_lat = lat + distance_metric
    return [
        min_long,
        min_lat,
        max_long,
        max_lat
    ]


def ca_postal_code_to_location_data(postal_code):
    if len(postal_code) == 6:
        postal_code = postal_code[:3] + ' ' + postal_code[3:]
    return CA_NOMI.query_postal_code(postal_code).to_dict()
