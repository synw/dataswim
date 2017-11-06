# -*- coding: utf-8 -*-

import pandas as pd
from numpy import NaN, where
from .db import Db
from .charts import Plot
from .data.views import View
from .data.clean import Clean
from .data.count import Count


class Transform():
    """
    Class to transform data
    """

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df

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
        Resample the main dataframe to a time period and optionaly create
        a date column from the datetime index
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


class Df(View, Transform, Clean, Count):
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

    def new(self, df):
        """
        Returns a new instance of DataSwim from a dataframe
        """
        return DataSwim(df)

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

    def csv(self, path):
        """
        Saves the main dataframe to a csv file
        """
        self.df.to_csv(path, encoding='utf-8')

    def load_csv(self, url):
        """
        Initialize the main dataframe from csv data
        """
        self.df = pd.read_csv(url)


class DataSwim(Plot, Db, Df):
    """
    Main class
    """
    pass


ds = DataSwim()
