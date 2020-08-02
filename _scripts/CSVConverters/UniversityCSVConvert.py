from CSVConvert import CSVToSQLConverter
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKeyConstraint

Base = declarative_base()

class UniversityConverter(CSVToSQLConverter):
    """
    Convert University data to University SQL Table.
    """
    def __init__(self, host, user, password, csv_path):
        super(UniversityConverter, self).__init__(host, user, password, csv_path)

    def __process__(self, df) -> pd.DataFrame:
        # Clean Institution to (universityName, campus)
        universities = df['Institution'].str.split(' - ')
        uni_names = []
        campuses = []
        for uni in universities:
            uni_names.append(uni[0])
            campuses.append(uni[1] if len(uni) > 1 else 'Main')

        # Mapping CSV to SQL Table
        table = {
            'universityName':  pd.Series(uni_names),
            'campus': pd.Series(campuses),
            'institutionType': df['Type'].copy(),
            'postalCode': df['Postal Code'].copy().str.split(' ').str.join(''),
            'city': df['City'].copy(),
            'province': df['Province'].copy(),
            'longitude': df['longitude'].copy(),
            'latitude': df['latitude'].copy(),
            'averageEC': df['Avg EC'].copy(),
            'averageNG': df['Avg NG'].copy()
        }

        sql_table = pd.DataFrame(table)

        return sql_table

    def commit(self):
        print('Commiting...')
        super(UniversityConverter, self).commit(name='University')

# class UniversityUpdater(UniversityConverter):
#     class University(Base):
#         __tablename__ = 'University'

#         id = Column(Integer, primary_key=True)
#         universityName = Column(String)
#         campus = Column(String)
#         institutionType = Column(String)
#         postalCode = Column(String)
#         city = Column(String)
#         province = Column(String)
#         longitude = Column(Float)
#         latitude = Column(Float)
    

#     def __init__(self, host, user, password, csv_path):
#         super(UniversityUpdater, self).__init__(host, user, password, csv_path)
#         from sqlalchemy.orm import sessionmaker
#         Session = sessionmaker(bind=self.engine)
#         self.session = Session()

#     def __process__(self, df) -> pd.DataFrame:
#         new_table = super(UniversityUpdater, self).__process__(df)
#         for uni in self.session.query(self.University).all():
#             #print(uni.universityName, uni.campus)
#             df_row = new_table[(new_table['universityName'] == uni.universityName) & (new_table['campus']==uni.campus)]
#             longitude = df_row['longitude'].item()
#             latitude = df_row['latitude'].item()
#             if str(longitude) != 'nan':
#                 uni.longitude = longitude
#             if str(latitude) != 'nan':
#                 uni.latitude = latitude
#             print(longitude, latitude, str(longitude) == 'nan', type(longitude))
#         self.session.commit()
#         print('Successful')

#     def __exc_sql__(self, df, name=None):
#         pass
    

# class AverageUtilityFeeConverter(UniversityConverter):
#     class AverageUtilityFee(Base):
#         __tablename__ = 'AverageUtilityFee'
#         __table_args__ = (
#             ForeignKeyConstraint(['universityId'], ['University.id']),
#         )

#         universityId = Column(Integer, primary_key=True)
#         averageEC = Column(Float)
#         averageNG = Column(Float)
#         averageHD = Column(Float)


#     def __init__(self, host, user, password, csv_path):
#         super(AverageUtilityFeeConverter, self).__init__(host, user, password, csv_path)
#         from sqlalchemy.orm import sessionmaker
#         Session = sessionmaker(bind=self.engine)
#         self.session = Session()

#     def __process__(self, df) -> pd.DataFrame:
#         new_table = super(AverageUtilityFeeConverter, self).__process__(df)
#         utility_fees = []

#         for uni in self.session.query(UniversityUpdater.University).all():
#             #print(uni.universityName, uni.campus)
#             df_row = new_table[(new_table['universityName'] == uni.universityName) & (new_table['campus']==uni.campus)]
#             ec = df_row['averageEC'].item()
#             ng = df_row['averageNG'].item()
#             if str(ec) == 'nan':
#                 ec = None
#             if str(ng) == 'nan':
#                 ng = None
            
#             utility_fees.append(self.AverageUtilityFee(universityId=uni.id, averageEC=ec, averageNG=ng))

#         self.session.add_all(utility_fees)
#         self.session.commit()
#         print('Successful')

#     def __exc_sql__(self, df, name=None):
#         pass

