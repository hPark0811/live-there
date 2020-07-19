"""This files will later be merged to collect.py. Running this file will update pgeo_data.csv fro data.csv"""
import pgeocode
import pandas as pd
import os

data_path = os.path.join(os.getcwd(), 'data.csv')

if __name__ == '__main__':
    df = pd.read_csv(data_path)
    postal_codes = list(df['Postal Code'])

    # Retrieve Longitude/Latitude ++ data with postal code
    nomi = pgeocode.Nominatim('ca')
    t = nomi.query_postal_code(postal_codes)

    # Concatenate DataFrame and save it.
    result = pd.concat([df, t], axis=1)
    result.to_csv('pgeo_data.csv')