from CSVConvert import CSVToSQLConverter
import pandas as pd


class UniversityConverter(CSVToSQLConverter):
    def __init__(self, host, user, password, csv_path):
        super(UniversityConverter, self).__init__(host, user, password, csv_path)

    def __process__(self, df) -> pd.DataFrame:
        universities = df['Institution'].str.split(' - ')
        uni_names = []
        campuses = []
        for uni in universities:
            uni_names.append(uni[0])
            campuses.append(uni[1] if len(uni) > 1 else None)

        table = {
            'universityName':  pd.Series(uni_names),
            'campus': pd.Series(campuses),
            'institutionType': df['Type'].copy(),
            'postalCode': df['Postal Code'].copy().str.split(' ').str.join(''),
            'city': df['City'].copy(),
            'province': df['Province'].copy()
        }
        sql_table = pd.DataFrame(table)

        return sql_table

    def commit(self):
        super(UniversityConverter, self).commit(name='University')
