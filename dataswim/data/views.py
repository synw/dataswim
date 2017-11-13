# -*- coding: utf-8 -*-

import pandas as pd
from pandas_profiling import ProfileReport
from goerr.colors import colors


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
        Display info about a dataframe
        """
        try:
            if dataframe is None:
                df = self.df
            if df is None:
                self.warning("Dataframe is empty: nothing to show")
                return
            num = len(df.index)
        except Exception as e:
            self.err(e, self.show, "Can not show dataframe")
            return
        f = list(df)
        num_fields = len(f)
        fields = ", ".join(f)
        if self.autoprint is True:
            self.info("The dataframe has", colors.bold(num), "rows and",
                      colors.bold(num_fields), "columns:")
            print(fields)
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

    def pvals(self, field):
        """
        Print the values count of a column     
        """
        return self._vals(field)

    def vals_(self, field, index_col="index"):
        """
        Returns a DatasWim instance from values count of a column     
        """
        ds2 = self.duplicate(df=self._vals(field))
        ds2.index_col(index_col)
        return ds2

    def _vals(self, field):
        """
        Returns a DatasWim instance from values count of a column     
        """
        if self.df is None:
            self.warning("Dataframe is empty: no values to show")
            return
        count = self.df[field].value_counts()
        df = pd.DataFrame(count)
        return df
