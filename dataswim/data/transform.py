# -*- coding: utf-8 -*-

import pandas as pd


class Transform():
    """
    Class to transform data
    """

    def __init__(self, df=None, db=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df
        self.db = db

    def reduce_(self, *fields):
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

    def resample_(self, time_period="1Min"):
        """
        Resample the main dataframe to a time period and optionaly create
        a date column from the datetime index
        """
        try:
            df = self.df.resample(time_period)
        except Exception as e:
            self.err(e)
            return
        return df

    def rsum(self, time_period="1Min", index_col=True, fill_col=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        try:
            self = self._rsum(time_period, True, index_col, fill_col)
        except Exception as e:
            self.err(e)
        return self

    def rsum_(self, time_period="1Min", index_col=True, fill_col=None):
        """
        Resample, and sum a dataframe to a time period
        """
        try:
            ds = self._rsum(time_period, False, index_col, fill_col)
        except Exception as e:
            self.err(e)
            return self
        return ds

    def _rsum(self, time_period, main, index_col=True, fill_col=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        try:
            df = self.df.resample(time_period).sum()
            self._index_fill(index_col, fill_col)
        except Exception as e:
            self.err(e)
        if main is True:
            self.df = df.copy()
            return self
        else:
            return self.new(df)

    def rmean(self, time_period="1Min", index_col=None, fill_col=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        try:
            self = self._rmean(time_period, True, index_col, fill_col)
        except Exception as e:
            self.err(e)

    def rmean_(self, time_period="1Min", index_col=None, fill_col=None):
        """
        Resample, and sum a dataframe to a time period
        """
        try:
            ds = self._rmean(time_period, False, index_col, fill_col)
        except Exception as e:
            self.err(e)
        return ds

    def _rmean(self, time_period, main, index_col=None, fill_col=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        try:
            df = self.df.resample(time_period).mean()
            self._index_fill(index_col, fill_col)
        except Exception as e:
            self.err(e)
        if main is True:
            self.df = df.copy()
            return self
        else:
            return self.new(df)

    def revert(self):
        """
        Reverts the main dataframe order
        """
        self.df = self.df.iloc[::-1]

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

    def index_col(self, field="date"):
        """
        Add a column from the index
        """
        try:
            self.df[field] = self.df.index.values
        except Exception as e:
            self.err(e)

    def rename(self, source_col, dest_col):
        """
        Renames a column in the main dataframe
        """
        self.df = self.df.rename(columns={source_col: dest_col})
