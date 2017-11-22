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
            n = self.df[field].isnull().sum()
        except KeyError:
            self.warning("Can not find column", field)
            return
        except Exception as e:
            self.err(e, self.count_nulls, "Can not count nulls")
            return
        if self.autoprint is True:
            self.ok("Found", n, "nulls in column", field)

    def count(self):
        """
        Counts the number of rows of the main dataframe
        """
        try:
            num = self._count()
        except Exception as e:
            self.err(e, self.count, "Can not count data")
            return
        if self.autoprint is True:
            self.ok("Found", num, "rows in the dataframe")

    def count_(self):
        """
        Returns the number of rows of the main dataframe
        """
        try:
            num = self._count()
        except Exception as e:
            self.err(e, self.count_, "Can not count data")
            return
        return num

    def _count(self):
        """
        Count the number of rows of the main dataframe
        """
        try:
            num = len(self.df.index)
            return num
        except Exception as e:
            self.err(e)
            return

    def count_empty(self, field):
        """
        List of empty row indices
        """
        try:
            df2 = self.keep_(field).df
            vals = where(df2.applymap(lambda x: x == ''))
            num = len(vals[0])
            return num
        except Exception as e:
            self.err(e, self.count_empty, "Can not count empty values")
            return
        if self.autoprint is True:
            self.ok("Found", num, "empty rows in the dataframe")

    def count_zero(self, field):
        """
        List of row with 0 values
        """
        try:
            df2 = self.keep_(field).df
            vals = where(df2.applymap(lambda x: x == 0))
            num = len(vals[0])
            return num
        except Exception as e:
            self.err(e, self.count_zero, "Can not count zero values")
        if self.autoprint is True:
            self.ok("Found", num, "zero values rows in column", field)

    def count_unique(self, field):
        """
        Return the number of unique values in a column     
        """
        try:
            num = self.df[field].nunique()
            return num
        except Exception as e:
            self.err(e, self.count_unique, "Can not count unique values")
        if self.autoprint is True:
            self.ok("Found", num, "unique values rows in column", field)
