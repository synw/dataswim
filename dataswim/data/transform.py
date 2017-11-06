# -*- coding: utf-8 -*-

import pandas as pd


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
            return self.new(df.copy())

    def exact(self, value, field, main=True):
        """
        Returns rows that has the exact string value in a column
        """
        df = self.df[self.df[field].isin([value])]
        if main is True:
            self.df = df
        else:
            return self.new(df.copy())

    def get_reduce(self, *fields):
        """
        Limit a dataframe to some columns
        """
        return self.new(self.df[list(fields)].copy())

    def reduce(self, *fields):
        """
        Limit a dataframe to some columns
        """
        self.df = self.df[list(fields)].copy()

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

    def apply(self, function):
        """
        Apply a function on a column's values
        """
        self.df = self.df.apply(function, axis=1)

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
