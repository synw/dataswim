# -*- coding: utf-8 -*-

import pandas as pd


class Clean():
    """
    Class to clean the data
    """

    def drop_nan(self, field=None):
        """
        Drop NaN values from the main dataframe
        """
        if field is None:
            self.df = self.df.dropna(how='all')
        else:
            self.df[field] = self.df[field].dropna(how='all')

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

    def fill_nulls(self, field):
        """
        Fill all null values with NaN values
        """
        n = [None, ""]
        self.df[field] = self.df[field].replace(n, NaN)

    def clean_ts(self, date_col, numeric_col):
        """
        Cleans and format a timeseries dataframe
        """
        self.fill(numeric_col)
        self.to_int(numeric_col)
        self.date_col(date_col)

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
