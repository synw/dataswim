# -*- coding: utf-8 -*-

from numpy import where


class Count():
    """
    Class to count data
    """

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df

    def count_nulls(self, field):
        """
        Count the number of null values in a rows
        """
        return self.df[field].isnull().sum()

    def count(self):
        """
        Count the number of rows of the main dataframe
        """
        return len(self.df.index)

    def count_empty(self, field):
        """
        Returns a list of empty row indices
        """
        df2 = self.reduce([field]).df
        vals = where(df2.applymap(lambda x: x == ''))
        return len(vals[0])

    def count_unique(self, field):
        """
        Return the number of unique values in a column     
        """
        return self.df[field].nunique()
