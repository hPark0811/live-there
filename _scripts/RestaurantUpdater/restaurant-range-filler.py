from utility import geo, sql
import geopy.distance


def get_distance_between_uni_and_restaurant(university, restaurant):
    uni_location = geo.ca_postal_code_to_location_data(university['postalCode'])
    restaurant_coord = (restaurant['longitude'], restaurant['latitude'])
    uni_coord = (uni_location['longitude'], uni_location['latitude'])

    try:
        return geopy.distance.distance(restaurant_coord, uni_coord).km
    except:
        return -1


def generate_sql_insert_field(uni_id, restaurant_id, distance_km):
    return (
        uni_id,
        restaurant_id,
        distance_km
    )


if __name__ == "__main__":
    dbms = sql.RentalDBMS()

    restaurant_df = dbms.get_all_restaurant_locations()
    universities_df = dbms.get_all_university_postal_codes()

    for universityNdx, university in universities_df.iterrows():
        print('init mapping university: ' + str(university['id']))
        to_insert_list = []
        for rentalNdx, restaurant in restaurant_df.iterrows():
            uni_id = int(university['id'])
            restaurant_id = int(restaurant['restaurantId'])

            distance_km = get_distance_between_uni_and_restaurant(university, restaurant)

            if 20 > distance_km > 0:
                to_insert_list.append(
                    generate_sql_insert_field(uni_id, restaurant_id, distance_km)
                )

        dbms.cursor.executemany(sql.RESTAURANT_RANGE_INSERT_SQL, to_insert_list)
        dbms.commit()
        print('finished mapping university: ' + str(university['id']))
