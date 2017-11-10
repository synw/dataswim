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

    def keep_(self, *fields):
        """
        Limit a dataframe to some columns
        """
        try:
            return self.new(self.df[list(fields)].copy())
        except Exception as e:
            self.err(e)

    def keep(self, *fields):
        """
        Limit a dataframe to some columns
        """
        try:
            self.df = self.df[list(fields)].copy()
        except Exception as e:
            self.err(e)

    def drop(self, column):
        """
        Drops a column from the main dataframe
        """
        try:
            self.df = self.df.drop(column, axis=1)
        except Exception as e:
            self.err(e)

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

    def rsum(self, time_period="1Min", index=None, index_col=True, fill_col=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        try:
            self = self._rsum(time_period, index, index_col, fill_col)
        except Exception as e:
            self.err(e)

    def rsum_(self, time_period="1Min", index=None, index_col=True, fill_col=None):
        """
        Resample, and sum a dataframe to a time period
        """
        try:
            ds = self._rsum(time_period, index, index_col, fill_col)
        except Exception as e:
            self.err(e)
            return
        return ds

    def _rsum(self, time_period, index=None, index_col=True, fill_col=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        try:
            df = self.df.resample(time_period).sum()
            ds2 = self.duplicate(df=df)
            if index is True or index_col is True or fill_col is True:
                ds2 = ds2.index_fill_(index, index_col, fill_col, quiet=True)
            return ds2
        except Exception as e:
            self.err(e)
            return

    def rmean(self, time_period="1Min", index=None, index_col=None, fill_col=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        try:
            self = self._rmean(time_period, index, index_col, fill_col)
        except Exception as e:
            self.err(e)

    def rmean_(self, time_period="1Min", index=None, index_col=None, fill_col=None):
        """
        Resample, and sum a dataframe to a time period
        """
        try:
            ds = self._rmean(time_period, index, index_col, fill_col)
        except Exception as e:
            self.err(e)
            return
        return ds

    def _rmean(self, time_period, index, index_col, fill_col):
        """
        Resample, and sum the main dataframe to a time period
        """
        try:
            df = self.df.resample(time_period).mean()
            ds2 = self.duplicate(df=df)
            if index is not None or index_col is not None or fill_col is not None:
                ds2 = ds2.index_fill_(index, index_col, fill_col, quiet=True)
            return ds2
        except Exception as e:
            self.err(e)

    def revert(self):
        """
        Reverts the main dataframe order
        """
        try:
            self.df = self.df.iloc[::-1]
        except Exception as e:
            self.err(e)

    def apply(self, function):
        """
        Apply a function on columns values
        """
        try:
            self.df = self.df.apply(function, axis=1)
        except Exception as e:
            self.err(e)

    def concat(self, *dfs):
        """
        Concatenate dataframes from a list and set it to the main dataframe
        """
        try:
            self.df = pd.concat(dfs)
        except Exception as e:
            self.err(e)

    def add(self, column, value):
        """
        Add a columns with default values
        """
        try:
            self.df[column] = value
        except Exception as e:
            self.err(e)

    def index_col(self, column="date"):
        """
        Add a column filled from the index to the main dataframe
        """
        try:
            self.df = self._index_col(column)
        except Exception as e:
            self.err(e)

    def index_col_(self, column="date"):
        """
        Returns a DatasWim instance with a new column filled from the index
        """
        try:
            df = self._index_col(column)
            return self.duplicate(df=df)
        except Exception as e:
            self.err(e)

    def _index_col(self, column):
        """
        Add a column from the index
        """
        df = self.df.copy()
        try:
            df[column] = df.index.values
            if self.autoprint is True:
                self.ok("Column", column, "added from index")
        except Exception as e:
            self.err(e)
        return df

    def rename(self, source_col, dest_col):
        """
        Renames a column in the main dataframe
        """
        try:
            self.df = self.df.rename(columns={source_col: dest_col})
        except Exception as e:
            self.err(e)
