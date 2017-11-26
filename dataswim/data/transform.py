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
            return self.clone_(self.df[list(fields)].copy())
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

    def drop(self, *cols):
        """
        Drops a column from the main dataframe
        """
        index = self.df.columns.values
        for col in cols:
            if col not in index:
                self.warning("Column", col, "not found. Aborting.")
                return
        try:
            for col in cols:
                self.df = self.df.drop(col, axis=1)
        except Exception as e:
            self.err(e, self.drop, "Can not drop column")

    def rsum(self, time_period="1Min", num_col="num", dateindex=None, index_col="date", fill_col=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        try:
            self.df = self._resample("sum", time_period,
                                     num_col, dateindex, index_col, fill_col)
        except Exception as e:
            self.err(e, self.rsum, "Can not sum data")

    def rsum_(self, time_period="1Min", num_col="num", dateindex=None, index_col="date", fill_col=None):
        """
        Resample, and sum a dataframe to a time period
        """
        try:
            df = self._resample("sum", time_period,
                                num_col, dateindex, index_col, fill_col)
            if num_col is not None:
                self.add(0, num_col)
        except Exception as e:
            self.err(e, self.rsum_, "Can not sum data")
            return
        return self.clone_(df)

    def _resample(self, method, time_period, num_col, dateindex, index_col, fill_col):
        """
        Resample the main dataframe to a time period
        """
        try:
            ds2 = self.clone_()
            if dateindex is not None:
                try:
                    ds2 = ds2.dateindex_(dateindex)
                    dateindex = None
                except Exception as e:
                    self.err(e, self._resample, "Can not process date index")
                    return
            if num_col is not None:
                ds2.add(num_col, 1)
            ds2.df = ds2.df.resample(time_period)
            if method == "sum":
                ds2.df = ds2.df.sum()
            elif method == "mean":
                ds2.df = ds2.df.mean()
            else:
                self.err(self._resample, "Resampling method " +
                         method + " unknown")
                return
            if self.autoprint is True:
                self.ok("Data resampled by", time_period)
            try:
                ds3 = self.transform_(None, index_col,
                                      fill_col, None, df=ds2.df)
            except Exception as e:
                self.err(e, self._resample,
                         "Can not transform data after resampling")
            return ds3.df
        except Exception as e:
            self.err(e, self._resample, "Can not resample data")
            return

    def rmean(self, time_period="1Min", num_col="num", dateindex=None, index_col="date", fill_col=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        try:
            self.df = self._resample("mean", time_period,
                                     num_col, dateindex, index_col, fill_col)
        except Exception as e:
            self.err(e, self.rmean, "Can not mean data")

    def rmean_(self, time_period="1Min", num_col="num", dateindex=None, index_col="date", fill_col=None):
        """
        Resample, and sum a dataframe to a time period
        """
        try:
            df = self._resample("mean", time_period,
                                num_col, dateindex, index_col, fill_col)
        except Exception as e:
            self.err(e, self.rmean_, "Can not mean data")
            return
        return self.clone_(df)

    def sum_(self, column):
        """
        Returns the sum of all values in a column
        """
        try:
            df = self.df[column]
            num = df.sum()
            return num
        except Exception as e:
            self.err(e, self.sum_, "Can not sum data on column " + column)

    def reverse(self):
        """
        Reverses the main dataframe order
        """
        try:
            self.df = self.df.iloc[::-1]
        except Exception as e:
            self.err(e, self.reverse, "Can not reverse the dataframe")

    def sort(self, column):
        """
        Sorts the main dataframe according to the given column
        """
        try:
            self.df = self.df.copy().sort_values(column)
        except Exception as e:
            self.err(e, self.reverse,
                     "Can not sort the dataframe from column " + column)

    def apply(self, function, cols=None, axis=1):
        """
        Apply a function on columns values
        """
        try:
            if cols is None:
                obj = self.df
                self.df = obj.apply(function, axis=axis)
            else:
                obj = self.df[cols]
                self.df[cols] = obj.apply(function, axis=axis)
        except Exception as e:
            self.err(e, self.apply, "Can not apply function")

    def pivot(self, index, columns, values):
        """
        Pivots a dataframe
        """
        try:
            self.df = self._pivot(index, columns, values)
        except Exception as e:
            self.err(e, self._pivot, "Can not pivot table")

    def pivot_(self, index, columns, values):
        """
        Pivots a dataframe
        """
        try:
            return self.clone_(self._pivot(index, columns, values))
        except Exception as e:
            self.err(e, self._pivot, "Can not pivot table")

    def _pivot(self, index, columns, values):
        """
        Pivots a dataframe
        """
        try:
            return self.df.pivot(index=index, columns=columns, values=values)
        except Exception as e:
            self.err(e, self._pivot, "Can not pivot table")

    def concat(self, *dfs):
        """
        Concatenate dataframes from a list and set it to the main dataframe
        """
        try:
            self.df = pd.concat(dfs)
        except Exception as e:
            self.err(e, self.concat, "Can not concatenate data")

    def split_(self, col):
        """
        Split the main dataframe according to column values
        """
        df = self.df.copy()
        try:
            dss = {}
            unique = df[col].unique()
            for key in unique:
                df2 = df.loc[df[col] == key]
                ds2 = self.clone_(df2)
                dss[key] = ds2
            return dss
        except Exception as e:
            self.err(e, self.unique, "Can not split dataframe")

    def add(self, column, value):
        """
        Add a columns with default values
        """
        try:
            df = self.df.copy()
            df[column] = value
            self.df = df
        except Exception as e:
            self.err(e, self.add, "Can not add column")

    def copy_col(self, origin_col, end_col):
        """
        Copy a columns values in another column
        """
        try:
            df = self.df.copy()
            df[end_col] = df[[origin_col]]
            self.df = df
        except Exception as e:
            self.err(e, self.copy_col, "Can not copy column")

    def index_col(self, column="index"):
        """
        Add a column filled from the index to the main dataframe
        """
        try:
            self.df = self._index_col(column)
        except Exception as e:
            self.err(e, self.index_col, "Can not add index column")

    def index_col_(self, column="index"):
        """
        Returns a DatasWim instance with a new column filled from the index
        """
        try:
            df = self._index_col(column)
            return self.clone_(df=df)
        except Exception as e:
            self.err(e, self.index_col_, "Can not add index column")

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
            self.err(e)

    def rename(self, source_col, dest_col):
        """
        Renames a column in the main dataframe
        """
        try:
            self.df = self.df.rename(columns={source_col: dest_col})
        except Exception as e:
            self.err(e, self.rename, "Can not rename column")
            return
        if self.autoprint is True:
            self.ok("Column", source_col, "renamed")
