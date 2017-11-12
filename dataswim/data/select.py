# -*- coding: utf-8 -*-

import pandas as pd
from goerr.colors import colors


class Select():
    """
    Class to select data
    """

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df

    def duplicate_(self, df=None, db=None):
        """
        Returns a new DataSwim instance using the previous database connection
        """
        if db is None:
            db = self.db
        if df is None:
            df = self.df.copy()
        ds2 = self.new_(df, db)
        if self.autoprint is True:
            self.ok("A duplicated instance was created")
        return ds2

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
        if dateindex is not None and index_col is not None and fill_col is not None:
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
        if self.autoprint is True:
            self.ok("Dataframe backed up")

    def restore(self):
        """
        Restore the main dataframe
        """
        try:
            self.df = self._restore()
        except Exception as e:
            self.err(e)

    def restore_(self):
        """
        Returns the restored main dataframe in a DataSwim instance
        """
        try:
            return self.duplicate_(self._restore())
        except Exception as e:
            self.err(e)

    def _restore(self):
        """
        Restore the main dataframe
        """
        if self.backup_df is None:
            self.warning("No dataframe is backed up: nothing restore")
            return
        try:
            return self.backup_df
        except Exception as e:
            self.err(e)
        if self.autoprint is True:
            self.ok("Dataframe is restored")

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
            return self.duplicate_(df.copy())
        except KeyError:
            self.err("Can not find " + colors.bold(column) + " column")
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
            return self.duplicate_(df)
        except KeyError:
            self.err("Can not find " + colors.bold(column) + " column")
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
            return self.duplicate_(df=df)
        except Exception as e:
            self.err(e)
        return self.duplicate(df)

    def to_records_(self):
        """
        Returns a list of dictionary records from the main dataframe
        """
        try:
            dic = self.df.to_dict(orient="records")
            return dic
        except Exception as e:
            self.err(e)

    def nulls_(self):
        """
        Return all null rows
        """
        null_rows = self.df[self.df.isnull().any(axis=1)]
        return null_rows
