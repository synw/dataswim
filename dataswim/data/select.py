# -*- coding: utf-8 -*-


class Select():
    """
    Class to select data
    """

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df

    def first(self, main=True):
        """
        Select the first row
        """
        if main is True:
            return self.df.iloc[0]
        else:
            return self.df.iloc[0]

    def limit(self, r=5, main=True):
        """
        Limit selection the a range
        """
        if main is True:
            self.df = self.df[:r]
        else:
            return self.df[:r]

    def contains(self, value, field, main=True):
        """
        Returns rows that contains a string value in a column
        """
        df = self.df[self.df[field].str.contains(value) == True]
        if main is True:
            self.df = df
        else:
            return self.new(df.copy())

    def exact(self, value, field, main=True):
        """
        Returns rows that has the exact string value in a column
        """
        df = self.df[self.df[field].isin([value])]
        if main is True:
            self.df = df
        else:
            return self.new(df.copy())
