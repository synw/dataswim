# -*- coding: utf-8 -*-

import pandas as pd


class Transform():
    """
    Class to transform data
    """

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

    def resample(self, time_period="1Min"):
        """
        Resample the main dataframe to a time period and optionaly create
        a date column from the datetime index
        """
        df = self.df.resample(time_period)
        return df

    def rsum(self, time_period="1Min"):
        """
        Resample, and sum the main dataframe to a time period
        """
        self.df = self._rsum(time_period, True)

    def get_rsum(self, time_period="1Min"):
        """
        Resample, and sum a dataframe to a time period
        """
        return self._rsum(time_period, False)

    def _rsum(self, time_period, main):
        """
        Resample, and sum the main dataframe to a time period
        """
        df = self.df.resample(time_period).sum()
        if main is True:
            return df
        else:
            return self.new(df)

    def apply(self, function):
        """
        Apply a function on columns values
        """
        self.df = self.df.apply(function, axis=1)

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
