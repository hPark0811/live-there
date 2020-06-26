import pgeocode
import pandas as pd
import os

data_path = os.path.join(os.getcwd(), 'data.csv')
if __name__ == '__main__':
    df = pd.read_csv(data_path)
    postal_codes = list(df['Postal Code'])
    nomi = pgeocode.Nominatim('ca')
    t = nomi.query_postal_code(postal_codes)
    result = pd.concat([df, t], axis=1)
    result.to_csv('pgeo_data.csv')