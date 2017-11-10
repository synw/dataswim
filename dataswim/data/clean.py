# -*- coding: utf-8 -*-

import pandas as pd


class Clean():
    """
    Class to clean the data
    """

    def drop_nan(self, field=None):
        """
        Drop NaN values from the main dataframe when the whole row is NaN
        """
        try:
            if field is None:
                self.df = self.df.dropna(how='all')
            else:
                self.df[field] = self.df[field].dropna(how='all')
        except Exception as e:
            self.err(e)

    def nan_empty(self, field):
        """
        Fill empty values with NaN values
        """
        try:
            self.df[field] = self.df[field].replace('', NaN)
        except Exception as e:
            self.err(e)

    def fill_nan(self, fields, val=0):
        """
        Fill NaN values with new values either from a list of columns or a 
        single column name string
        """
        self.df = self._fill_nan(fields, val)

    def fill_nan_(self, fields, val=0):
        """
        Returns a DataSwim instance with NaN values flled with new values either from 
        a list of columns or a single column name string
        """
        df = self._fill_nan(fields, val)
        return self.duplicate(df=df)

    def _fill_nan(self, fields, val=0):
        """
        Fill NaN values with new values either from a list of columns or a 
        single column name string
        """
        df = self.df.copy()
        if type(fields) == str:
            try:
                df[fields] = df[fields].fillna(val)
            except Exception as e:
                self.err(e)
        else:
            print("FIELDS", fields)
            try:
                for el in fields:
                    df[el] = df[el].fillna(val)
            except Exception as e:
                self.err(e)
        return df

    def fill_nulls(self, field):
        """
        Fill all null values with NaN values
        """
        n = [None, ""]
        try:
            self.df[field] = self.df[field].replace(n, NaN)
        except Exception as e:
            self.err(e)

    def clean_ts(self, date_col, numeric_col=None, index=True, to_int=False, index_col=True):
        """
        Cleans and format a timeseries dataframe
        """
        try:
            self.date(date_col)
            if index is True:
                self.index(date_col)
            if numeric_col is not None:
                self.fill_nan(numeric_col)
                if to_int is True:
                    self.to_int(numeric_col)
            if index_col is True:
                self.index_col()
            self.index_col(date_col)
        except Exception as e:
            self.err(e)

    def date(self, fields):
        """
        Convert column values to datetime from either a list 
        of column names or a single column name string
        """
        try:
            if type(fields) == str:
                self.df[fields] = pd.to_datetime(self.df[fields]).apply(
                    lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                for f in fields:
                    self.df[f] = pd.to_datetime(self.df[f]).apply(
                        lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            self.err(e)

    def dateindex(self, datafield, indexfield="date_index"):
        """
        Set a datetime index from a column
        """
        try:
            self.df = self._dateindex(datafield, indexfield)
        except Exception as e:
            self.err(e)

    def dateindex_(self, datafield, indexfield="date_index"):
        """
        Returns a DataSwim instance index from a column
        """
        try:
            df = self._dateindex(datafield, indexfield)
        except Exception as e:
            self.err(e)
            return
        return self.duplicate(df=df)

    def _dateindex(self, datafield, indexfield):
        """
        Returns a datetime index from a column
        """
        df = self.df.copy()
        try:
            df = df.set_index(pd.DatetimeIndex(df[datafield]))
        except Exception as e:
            msg = "Can not reindex with datafield " + \
                datafield + " and indexfield " + indexfield
            self.err(e, msg)
            return
        return df

    def to_int(self, *fields):
        """
        Convert some columns values to integers
        """
        try:
            for el in fields:
                self.df[el] = self.df[el].apply(lambda x: int(x))
        except Exception as e:
            self.err(e)

    def index_fill(self, index=None, index_col=None, fill_col=None, quiet=False):
        """
        Add a column from index and/or fill nans in a column
        """
        try:
            self = self._index_fill(index, index_col, fill_col, quiet)
        except Exception as e:
            self.err(e)

    def index_fill_(self, index=None, index_col=None, fill_col=None, quiet=False):
        """
        Returns a DataSwim instance with a column from index and/or fill nans in a column
        """
        try:
            return self._index_fill(index, index_col, fill_col, quiet)
        except Exception as e:
            self.err(e)

    def _index_fill(self, index, index_col, fill_col, quiet):
        """
        Add a column from index and/or fill nans in a column
        """
        if index is None and index_col is None and fill_col is None and quiet is False:
            if quiet is False:
                self.debug(
                    "Method index_fill: please provide at least one parameter")
            return
        ds2 = self.duplicate()
        if index is not None:
            try:
                ds2 = ds2.dateindex_(index)
            except Exception as e:
                self.err(e)
                return
        if index_col is not None:
            try:
                ds2 = ds2.index_col_(index_col)
            except Exception as e:
                self.err(e)
                return
        if fill_col is not None:
            try:
                ds2 = ds2.fill_nan_(fill_col)
            except Exception as e:
                self.err(e)
                return
        return ds2
