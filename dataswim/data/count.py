# -*- coding: utf-8 -*-
from numpy import where


class Count():
    """
    Class to count data
    """

    def count_nulls(self, field):
        """
        Count the number of null values in a column
        """
        try:
            n = self.df[field].isnull().sum()
        except KeyError:
            self.warning("Can not find column", field)
            return
        except Exception as e:
            self.err(e, "Can not count nulls")
            return
        self.ok("Found", n, "nulls in column", field)

    def count(self):
        """
        Counts the number of rows of the main dataframe
        """
        try:
            num = len(self.df.index)
        except Exception as e:
            self.err(e, "Can not count data")
            return
        self.ok("Found", num, "rows in the dataframe")

    def count_(self):
        """
        Returns the number of rows of the main dataframe
        """
        try:
            num = len(self.df.index)
        except Exception as e:
            self.err(e, "Can not count data")
            return
        return num

    def count_empty(self, field):
        """
        List of empty row indices
        """
        try:
            df2 = self.df[[field]]
            vals = where(df2.applymap(lambda x: x == ''))
            num = len(vals[0])
        except Exception as e:
            self.err(e, "Can not count empty values")
            return
        self.ok("Found", num, "empty rows in column " + field)

    def count_zero(self, field):
        """
        List of row with 0 values
        """
        try:
            df2 = self.df[[field]]
            vals = where(df2.applymap(lambda x: x == 0))
            num = len(vals[0])
        except Exception as e:
            self.err(e, "Can not count zero values")
            return
        self.ok("Found", num, "zero values in column", field)

    def count_unique_(self, field):
        """
        Return the number of unique values in a column
        """
        try:
            num = self.df[field].nunique()
            return num
        except Exception as e:
            self.err(e, "Can not count unique values")
            return
        self.ok("Found", num, "unique values in column", field)
