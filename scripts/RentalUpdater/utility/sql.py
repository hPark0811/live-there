import mysql.connector
import pandas as pd

CONFIG = {
    'HOST': "35.225.74.52",
    'USER': "root",
    'PASSWORD': "livethere2020",
    'DATABASE': "livethere"
}

RENTAL_INSERT_SQL = """
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

RENTAL_RANGE_INSERT_SQL = """
INSERT IGNORE INTO livethere.RentalRange
(`universityId`,
`rentalId`,
`rentToUniversityDistance`)
VALUES
(%s,
%s,
%s);
"""


class RentalDBMS:
    def __init__(self):
        self.db = mysql.connector.connect(
            host=CONFIG['HOST'],
            user=CONFIG['USER'],
            password=CONFIG['PASSWORD'],
            database=CONFIG['DATABASE']
        )

        self.cursor = self.db.cursor()

    def commit(self):
        self.db.commit()

    def get_all_rentals_locations(self):
        query = pd.read_sql_query(
            "SELECT id, longitude, latitude FROM Rental",
            self.db
        )

        return pd.DataFrame(query, columns=['id', 'longitude', 'latitude'])

    def get_all_university_postal_codes(self):
        query = pd.read_sql_query(
            "SELECT id, postalCode FROM University",
            self.db
        )

        return pd.DataFrame(query, columns=['id', 'postalCode'])
