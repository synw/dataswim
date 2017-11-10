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

    def rsum(self, time_period="1Min", index_col=True, fill_cols=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        try:
            self.df = self._rsum(time_period, True)
        except Exception as e:
            self.err(e)

    def rsum_(self, time_period="1Min", index_col=True, fill_cols=None):
        """
        Resample, and sum a dataframe to a time period
        """
        try:
            ds = self._rsum(time_period, False)
        except Exception as e:
            self.err(e)
            return
        return ds

    def _rsum(self, time_period, main, index_col=True, fill_cols=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        df = self.df.resample(time_period).sum()
        if index_col is True:
            try:
                self.index_col()
            except Exception as e:
                self.err(e)
                return
        if fill_cols is not None:
            try:
                self.fill(fill_cols)
            except Exception as e:
                self.err(e)
                return
        if main is True:
            return self
        else:
            return self.new(df)

    def rmean(self, time_period="1Min", index_col=True, fill_col=True):
        """
        Resample, and sum the main dataframe to a time period
        """
        self.df = self._rmean(time_period, True)
        if index_col is True:
            self.index_col()
        if fill_col is True:
            self.fill(fill_col)

    def rmean_(self, time_period="1Min", index_col=True, fill_col=True):
        """
        Resample, and sum a dataframe to a time period
        """
        ds = self._rmean(time_period, False)
        if index_col is True:
            ds.index_col()
        if fill_col is True:
            ds.fill(fill_col)
        return ds

    def _rmean(self, time_period, main):
        """
        Resample, and sum the main dataframe to a time period
        """
        df = self.df.resample(time_period).mean()
        if main is True:
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
