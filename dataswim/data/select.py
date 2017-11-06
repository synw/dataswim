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
