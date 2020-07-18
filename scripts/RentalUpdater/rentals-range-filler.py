from utility import geo, sql
import geopy.distance


def get_distance_between_uni_and_rental(university, rental):
    uni_location = geo.ca_postal_code_to_location_data(university['postalCode'])
    rental_coord = (rental['longitude'], rental['latitude'])
    uni_coord = (uni_location['longitude'], uni_location['latitude'])

    try:
        return geopy.distance.distance(rental_coord, uni_coord).km
    except:
        return -1


def generate_sql_insert_field(uni_id, rental_id, distance_km):
    return (
        uni_id,
        rental_id,
        distance_km
    )


if __name__ == "__main__":
    dbms = sql.RentalDBMS()

    rentals_df = dbms.get_all_rentals_locations()
    universities_df = dbms.get_all_university_postal_codes()

    for universityNdx, university in universities_df.iterrows():
        print('init mapping university: ' + str(university['id']))
        to_insert_list = []
        for rentalNdx, rental in rentals_df.iterrows():
            uni_id = int(university['id'])
            rental_id = int(rental['id'])

            distance_km = get_distance_between_uni_and_rental(university, rental)

            if 20 > distance_km > 0:
                to_insert_list.append(
                    generate_sql_insert_field(uni_id, rental_id, distance_km)
                )

        dbms.cursor.executemany(sql.RENTAL_RANGE_INSERT_SQL, to_insert_list)
        dbms.commit()
        print('finished mapping university: ' + str(university['id']))
