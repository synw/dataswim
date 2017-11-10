# -*- coding: utf-8 -*-

import pandas as pd
from goerr.colors import cols


class Select():
    """
    Class to select data
    """

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df

    def load_csv(self, url, dateindex=None, index_col=None, fill_col=None):
        """
        Initialize the main dataframe from csv data
        """
        try:
            self.df = self._load_csv(
                url, dateindex, index_col, fill_col).df
        except Exception as e:
            self.err(e, "Can not load csv file")

    def load_csv_(self, url, dateindex=None, index_col=None, fill_col=None):
        """
        Returns a DataSwim instance from csv data
        """
        try:
            return self._load_csv(url, dateindex, index_col, fill_col)
        except Exception as e:
            self.err(e, "Can not load csv file")

    def _load_csv(self, url, dateindex, index_col, fill_col):
        """
        Returns a DataSwim instance from csv data
        """
        try:
            df = pd.read_csv(url)
            ds2 = self.duplicate(df=df)
        except FileNotFoundError as e:
            msg = "File " + url + " not found"
            self.warning(msg)
            return
        except Exception as e:
            self.err(e)
            return
        ds2 = ds2.index_fill_(dateindex, index_col, fill_col, quiet=True)
        return ds2

    def set(self, df):
        """
        Set a main dataframe
        """
        try:
            self.df = df.copy()
        except Exception as e:
            self.err(e)

    def backup(self):
        """
        Backup the main dataframe
        """
        try:
            self.backup_df = self.df.copy()
        except Exception as e:
            self.err(e)

    def restore(self):
        """
        Restore the main dataframe
        """
        try:
            self.df = self.backup_df
        except Exception as e:
            self.err(e)

    def first(self):
        """
        Select the first row
        """
        try:
            return self.df.iloc[0]
        except Exception as e:
            self.err(e)

    def limit(self, r=5):
        """
        Limit selection the a range in the main dataframe
        """
        try:
            self.df = self.df[:r]
        except Exception as e:
            self.err(e)

    def limit_(self, r=5):
        """
        Returns a DataSwim instance with limited selection
        """
        try:
            return self.new(self.df[:r])
        except Exception as e:
            self.err(e)

    def unique(self, column):
        """
        Returns unique values in a colum
        """
        try:
            df = self.df[column].unique()
            return df
        except Exception as e:
            self.err(e)

    def contains_(self, column, value):
        """
        Returns rows that contains a string value in a column
        """
        try:
            df = self.df[self.df[column].str.contains(value) == True]
            return self.duplicate(df.copy())
        except KeyError:
            self.err("Can not find " + cols.BOLD +
                     column + cols.ENDC + " column")
            return
        except Exception as e:
            self.err(e)

    def exact_(self, column, *values):
        """
        Returns rows that has the exact string value in a column
        """
        try:
            df2 = self.df[column].isin(list(values))
            df = self.df[df2]
            return self.duplicate(df.copy())
        except KeyError:
            self.err("Can not find " + cols.BOLD +
                     column + cols.ENDC + " column")
            return
        except Exception as e:
            self.err(e)

    def range_(self, num, unit):
        """
        Limit the data in a time range
        """
        try:
            df = self.df[self.df.last_valid_index() -
                         pd.DateOffset(num, unit):]
            return self.duplicate(df=df)
        except Exception as e:
            self.err(e)

    def to_records_(self):
        """
        Returns a list of dictionary records from the main dataframe
        """
        try:
            dic = self.df.to_dict(orient="records")
            return dic
        except Exception as e:
            self.err(e)
