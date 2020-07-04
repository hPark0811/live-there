"""
This file contain CSVToSQL converter interface.
"""
from abc import ABC
import pandas as pd
from sqlalchemy import create_engine


class MySQLConnectionError(Exception):
    pass


class CSVToSQLConverter(ABC):
    def __init__(self, host, user, password, csv_path):
        self.csv_path = csv_path
        self.engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/livethere')

    def __csv__(self) -> pd.DataFrame:
        """
        Retrieve csv file as DataFrame
        :return:
        """
        return pd.read_csv(self.csv_path)

    def __process__(self, df) -> pd.DataFrame:
        """
        Create conversion.
        Any child should overwrite this function to map CSV df to proper df with proper SQL table format.
        :param df: raw DataFrame
        :return: df data with sql table fields as columns & data is properly formatted.
        """
        raise NotImplementedError('CSVToSQLConverter: Must implement exc_sql method')

    def __exc_sql__(self, df, name):
        """
        Convert DataFrame object and append it to the MySQL DB.
        :param name: name of DB
        :param df: cleaned DataFrame with proper fields name
        :return:
        """
        df.to_sql(con=self.engine, index=False, name=name, if_exists='append')

    def commit(self, name):
        """
        execute __exc_sql__
        :param name: name of DB
        :return:
        """
        self.__exc_sql__(self.__process__(self.__csv__()), name)
