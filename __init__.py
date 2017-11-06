# -*- coding: utf-8 -*-

import pandas as pd
from pandas_profiling import ProfileReport
from numpy import NaN, where
from .db import Db
from .charts import Plot


class Df():
    """
    Class for manipulating dataframes
    """

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df
        self.backup_df = df

    def set(self, df):
        """
        Set a main dataframe
        """
        self.df = df.copy()

    def backup(self):
        """
        Backup the main dataframe
        """
        self.backup_df = self.df.copy()

    def restore(self):
        """
        Restore the main dataframe
        """
        self.df = self.backup_df

    def save(self, path):
        """
        Saves the main dataframe to a csv file
        """
        self.df.to_csv(path, encoding='utf-8')

    def load_csv(self, url):
        """
        Initialize the main dataframe from csv data
        """
        self.df = pd.read_csv(url)

    def date(self, fields):
        """
        Convert column values to datetime from either a list 
        of column names or a single column name string
        """
        if type(fields) == str:
            self.df[fields] = pd.to_datetime(self.df[fields]).apply(
                lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            for f in fields:
                self.df[f] = pd.to_datetime(self.df[f]).apply(
                    lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

    def index(self, datafield, indexfield):
        """
        Set a datetime index from a column
        """
        f = {indexfield: self.df[datafield]}
        self.df = self.df.assign(**f)
        self.df = self.df.set_index(indexfield)
        self.df.index = pd.to_datetime(self.df.index)

    def contains(self, value, field, main=True):
        """
        Returns rows that contains a string value in a column
        """
        df = self.df[self.df[field].str.contains(value) == True]
        if main is True:
            self.df = df
        else:
            return DataSwim(df)

    def exact(self, value, field, main=True):
        """
        Returns rows that has the exact string value in a column
        """
        df = self.df[self.df[field].isin([value])]
        if main is True:
            self.df = df
        else:
            return DataSwim(df)

    def reduce(self, fields, main=True):
        """
        Limit a dataframe to some columns
        """
        df = self.df[fields].copy()
        if main is True:
            self.df = df
        else:
            return DataSwim(df)

    def drop(self, field):
        """
        Drops a column from the main dataframe
        """
        self.df = self.df.drop(field, axis=1)

    def resample(self, time_unit="1Min"):
        """
        Resample the main dataframe to a time period
        """
        df = self.df.resample(time_unit)
        return df

    def range(self, num, unit):
        """
        Limit the data in a time range
        """
        self.df = self.df[self.df.last_valid_index() -
                          pd.DateOffset(num, unit):]

    def concat(self, dfs):
        """
        Concatenate dataframes from a list and set it to the main dataframe
        """
        self.df = pd.concat(dfs)

    def add(self, field, value):
        """
        Add a columns with default values
        """
        self.df[field] = value

    def date_col(self, field):
        """
        Add a date column from the datetime index
        """
        self.df[field] = self.df.index.values

    def head(self, rows=5):
        """
        Returns the main dataframe's head
        """
        return self.df.head(rows)

    def tail(self, rows=5):
        """
        Returns the main dataframe's tail
        """
        return self.df.tail(rows)

    def look(self, df=None, p=True):
        """
        Returns basic data info
        """
        if df is None:
            df = self.df
        num = len(self.df.index)
        if p is True:
            print(num, "rows")
            print("Fields:", ", ".join(list(self.df)))
        else:
            return p

    def describe(self):
        """
        Return a description of the data
        """
        self.look()
        return self.df.describe()

    def report(self, df=None):
        """
        Returns a dataframe profiling report
        """
        if df is None:
            df = self.df
        return ProfileReport(df)

    def display(self, fields):
        """
        Display some columns head
        """
        if type(fields) == str:
            df2 = self.df[[fields]]
        else:
            df2 = self.df[fields]
        return df2.head()

    def vals(self, field):
        """
        Returns a values count of a column     
        """
        return self.df[field].value_counts()

    def drop_nan(self):
        """
        Drop NaN values from the main dataframe
        """
        self.df = self.df.dropna()

    def fill(self, fields, val=0):
        """
        Fill NaN values with new values either from a list of columns or a 
        single column name string
        """
        if type(fields) == str:
            self.df[fields] = self.df[fields].fillna(val)
        else:
            for el in fields:
                self.df[el] = self.df[el].fillna(val)

    def to_int(self, fields):
        """
        Convert a column values to integers either from a list of columns or a 
        single column name string
        """
        if type(fields) == str:
            self.df[fields] = self.df[fields].apply(lambda x: int(x))
        else:
            for el in fields:
                self.df[el] = self.df[el].apply(lambda x: int(x))

    def nan_empty(self, field):
        """
        Fill empty values with NaN values
        """
        self.df[field] = self.df[field].replace('', NaN)

    def fill_nulls(self, field):
        """
        Fill all null values with NaN values
        """
        n = [None, ""]
        self.df[field] = self.df[field].replace(n, NaN)

    def count_nulls(self, field):
        """
        Count the number of null values in a rows
        """
        return self.df[field].isnull().sum()

    def count(self):
        """
        Count the number of rows of the main dataframe
        """
        return len(self.df.index)

    def count_empty(self, field):
        """
        Returns a list of empty row indices
        """
        df2 = self.reduce([field]).df
        vals = where(df2.applymap(lambda x: x == ''))
        return len(vals[0])

    def count_unique(self, field):
        """
        Return the number of unique values in a column     
        """
        return self.df[field].nunique()


class DataSwim(Plot, Db, Df):
    """
    Main class
    """
    pass


ds = DataSwim()
