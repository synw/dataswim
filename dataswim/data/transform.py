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
            return self.duplicate_(self.df[list(fields)].copy())
        except Exception as e:
            self.err(e, self.keep_, "Can not remove colums")
        if self.autoprint is True:
            self.ok("Columns", " ,".join(fields), "kept")

    def keep(self, *fields):
        """
        Limit a dataframe to some columns
        """
        try:
            self.df = self.df[list(fields)].copy()
        except Exception as e:
            self.err(e, self.keep, "Can not remove colums")
        if self.autoprint is True:
            self.ok("Setting dataframe to columns", " ".join(fields))

    def drop(self, column):
        """
        Drops a column from the main dataframe
        """
        try:
            self.df = self.df.drop(column, axis=1)
        except Exception as e:
            self.err(e, self.drop, "Can not drop column")

    def rsum(self, time_period="1Min", dateindex=None, index_col=None, fill_col=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        try:
            self.df = self._resample("sum", time_period,
                                     dateindex, index_col, fill_col)
        except Exception as e:
            self.err(e, self.rsum, "Can not sum data")

    def rsum_(self, time_period="1Min", dateindex=None, index_col=None, fill_col=None):
        """
        Resample, and sum a dataframe to a time period
        """
        try:
            df = self._resample("sum", time_period,
                                dateindex, index_col, fill_col)
        except Exception as e:
            self.err(e, self.rsum_, "Can not sum data")
            return
        return self.duplicate_(df)

    def _resample(self, method, time_period, dateindex, index_col, fill_col):
        """
        Resample the main dataframe to a time period
        """
        try:
            ds2 = self.duplicate_()
            if dateindex is not None:
                ds2 = ds2.dateindex_(dateindex)
            ds2.df = ds2.df.resample(time_period)
            if method == "sum":
                ds2.df = ds2.df.sum()
            elif method == "mean":
                ds2.df = ds2.df.mean()
            else:
                self.err(self._resample, "Resampling method " +
                         method + " unknown")
            if self.autoprint is True:
                self.ok("Data resampled by", time_period)
            ds3 = ds2
            if fill_col is not None:
                ds3 = ds3.fill_nan_(0, fill_col)
            if index_col is not None:
                ds3 = ds3.index_col_(index_col)
            return ds3.df
        except Exception as e:
            self.err(e, self._resample, "Can not resample data")
            return

    def rmean(self, time_period="1Min", dateindex=None, index_col=None, fill_col=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        try:
            self.df = self._resample("mean", time_period,
                                     dateindex, index_col, fill_col)
        except Exception as e:
            self.err(e, self.rmean, "Can not mean data")

    def rmean_(self, time_period="1Min", dateindex=None, index_col=None, fill_col=None):
        """
        Resample, and sum a dataframe to a time period
        """
        try:
            df = self._resample("mean", time_period,
                                dateindex, index_col, fill_col)
        except Exception as e:
            self.err(e, self.rmean_, "Can not mean data")
            return
        return self.duplicate_(df)
    """
    def _rmean(self, time_period, dateindex, index_col, fill_col):
        ""
        Resample, and sum the main dataframe to a time period
        ""
        try:
            df = self.df.resample(time_period).mean()
            ds2 = self.duplicate_(df=df)
            if dateindex is not None or index_col is not None or fill_col is not None:
                ds2 = ds2.index_fill_(
                    dateindex, index_col, fill_col, quiet=True)
            return ds2
        except Exception as e:
            self.err(e, self._rmean, "Can not mean data")
    """

    def revert(self):
        """
        Reverts the main dataframe order
        """
        try:
            self.df = self.df.iloc[::-1]
        except Exception as e:
            self.err(e, self.revert)

    def apply(self, function):
        """
        Apply a function on columns values
        """
        try:
            self.df = self.df.apply(function, axis=1)
        except Exception as e:
            self.err(e, self.apply)

    def concat(self, *dfs):
        """
        Concatenate dataframes from a list and set it to the main dataframe
        """
        try:
            self.df = pd.concat(dfs)
        except Exception as e:
            self.err(e, self.concat)

    def add(self, column, value):
        """
        Add a columns with default values
        """
        try:
            self.df[column] = value
        except Exception as e:
            self.err(e, self.add)

    def index_col(self, column="index"):
        """
        Add a column filled from the index to the main dataframe
        """
        try:
            self.df = self._index_col(column)
        except Exception as e:
            self.err(e, self.index_col)

    def index_col_(self, column="index"):
        """
        Returns a DatasWim instance with a new column filled from the index
        """
        try:
            df = self._index_col(column)
            return self.duplicate_(df=df)
        except Exception as e:
            self.err(e, self.index_col_)

    def _index_col(self, column):
        """
        Add a column from the index
        """
        df = self.df.copy()
        try:
            df[column] = df.index.values
            if self.autoprint is True:
                self.ok("Column", column, "added from index")
            return df
        except Exception as e:
            self.err(e, self._index_col)

    def rename(self, source_col, dest_col):
        """
        Renames a column in the main dataframe
        """
        try:
            self.df = self.df.rename(columns={source_col: dest_col})
        except Exception as e:
            self.err(e, self.rename)
