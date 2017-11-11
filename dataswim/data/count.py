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
        try:
            return self.df[field].isnull().sum()
        except Exception as e:
            self.err(e, self.count_nulls)

    def count(self):
        """
        Count the number of rows of the main dataframe
        """
        try:
            return len(self.df.index)
        except Exception as e:
            self.err(e, self.count)

    def count_empty(self, field):
        """
        Returns a list of empty row indices
        """
        try:
            df2 = self.keep_(field).df
            vals = where(df2.applymap(lambda x: x == ''))
            return len(vals[0])
        except Exception as e:
            self.err(e, self.count_empty)

    def count_unique(self, field):
        """
        Return the number of unique values in a column     
        """
        try:
            return self.df[field].nunique()
        except Exception as e:
            self.err(e, self.count_unique)
