# -*- coding: utf-8 -*-

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
        return self.df.head(rows)

    def tail(self, rows=5):
        """
        Returns the main dataframe's tail
        """
        return self.df.tail(rows)

    def look(self, df=None, p=True):
        """
        Returns basic data info
        """
        if df is None:
            df = self.df
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
        self.look()
        return self.df.describe()

    def show(self, p=True, dataframe=None):
        """
        Display info about a table
        """
        if dataframe is None:
            df = self.df
        num = len(self.df.index)
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
        return ProfileReport(df)

    def display(self, fields):
        """
        Display some columns head
        """
        if type(fields) == str:
            df2 = self.df[[fields]]
        else:
            df2 = self.df[fields]
        return df2.head()

    def vals(self, field):
        """
        Returns a values count of a column     
        """
        return self.df[field].value_counts()
