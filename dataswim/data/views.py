# -*- coding: utf-8 -*-

import pandas as pd
from pandas_profiling import ProfileReport


class View():
    """
    Class to view the data
    """

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df

    def head(self, rows=5):
        """
        Returns the main dataframe's head
        """
        if self.df is None:
            self.warning("Dataframe is empty: no head available")
            return
        return self.df.head(rows)

    def tail(self, rows=5):
        """
        Returns the main dataframe's tail
        """
        if self.df is None:
            self.warning("Dataframe is empty: no tail available")
        return self.df.tail(rows)

    def look(self, df=None, p=True):
        """
        Returns basic data info
        """
        if df is None:
            df = self.df
        if df is None:
            self.warning("Dataframe is empty: nothing to look at")
            return
        num = len(self.df.index)
        if p is True:
            print(num, "rows")
            print("Fields:", ", ".join(list(self.df)))
        else:
            return p

    def describe(self):
        """
        Return a description of the data
        """
        if self.df is None:
            self.warning("Dataframe is empty: nothing to describe")
            return
        self.look()
        return self.df.describe()

    def show(self, p=True, dataframe=None):
        """
        Display info about a table
        """
        try:
            if dataframe is None:
                df = self.df
            if df is None:
                self.warning("Dataframe is empty: nothing to show")
                return
            num = len(self.df.index)
        except Exception as e:
            self.err(e)
            return
        if p is True:
            print(num, "rows")
            print("Fields:", ", ".join(list(df)))
        return df.head()

    def report(self, df=None):
        """
        Returns a dataframe profiling report
        """
        if df is None:
            df = self.df
        if self.df is None:
            self.warning("Dataframe is empty: nothing to report")
            return
        return ProfileReport(df)

    def display(self, *fields):
        """
        Display some columns head
        """
        if self.df is None:
            self.warning("Dataframe is empty: nothing to display")
            return
        df2 = self.df[list(fields)]
        return df2.head()

    def vals(self, field):
        """
        Set the main dataframe from values count of a column     
        """
        self._vals(field, inplace=True)

    def vals_(self, field):
        """
        Returns a DatasWim instance from values count of a column     
        """
        return self._vals(field, inplace=False)

    def _vals(self, field, inplace=True):
        """
        Returns a DatasWim instance from values count of a column     
        """
        if self.df is None:
            self.warning("Dataframe is empty: no values to show")
            return
        ds = self.new(pd.DataFrame(self.df[field].value_counts()))
        if inplace is True:
            self.df = ds.df
        else:
            return ds
