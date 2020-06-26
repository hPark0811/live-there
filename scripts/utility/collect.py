from utilities_fees import run_scraper
import pandas as pd
import os

INSTITUTION_CSV_PATH = os.path.join(os.getcwd(), 'education_institution.csv')


def main():
    df = pd.read_csv(INSTITUTION_CSV_PATH)
    df.dropna(inplace=True)
    postal_codes = list(df['Postal Code'])
    ec_bills, ng_bills = run_scraper(postal_codes)
    df['Avg EC'] = pd.Series(ec_bills, dtype='float64')
    df['Avg NG'] = pd.Series(ng_bills, dtype='float64')

    df.to_csv('data.csv')


if __name__ == '__main__':
    main()