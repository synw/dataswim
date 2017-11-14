# -*- coding: utf-8 -*-

import pandas as pd
from .views import View
from .clean import Clean
from .count import Count
from .select import Select
from .transform import Transform
from .export import Export
from .search import Search


class Df(Select, View, Transform, Clean, Count, Export, Search):
    """
    Class for manipulating dataframes
    """

    def __init__(self, df=None, db=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df

    def duplicate_(self, df=None, db=None, quiet=False):
        """
        Returns a new DataSwim instance using the previous database connection
        """
        if db is None:
            db = self.db
        if df is None:
            df = self.df.copy()
        ds2 = self.new_(df, db, quiet=True)
        if self.autoprint is True and quiet is False:
            self.ok("A duplicated instance was created")
        return ds2

    def clone_(self, df=None, db=None):
        """
        Silently clone the DataSwim instance
        """
        return self.duplicate_(df, db, quiet=True)

    def set(self, df):
        """
        Set a main dataframe
        """
        try:
            self.df = df.copy()
        except Exception as e:
            self.err(e, self.set, "Can not set the main dataframe")

    def backup(self):
        """
        Backup the main dataframe
        """
        try:
            self.backup_df = self.df.copy()
        except Exception as e:
            self.err(e, self.backup, "Can not backup data")
        if self.autoprint is True:
            self.ok("Dataframe backed up")

    def restore(self):
        """
        Restore the main dataframe
        """
        try:
            self.df = self._restore()
        except Exception as e:
            self.err(e, self.restore, "Can not restore dataframe")

    def restore_(self):
        """
        Returns the restored main dataframe in a DataSwim instance
        """
        try:
            return self.clone_(self._restore())
        except Exception as e:
            self.err(e, self.restore_, "Can not restore dataframe")

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

    def load_csv(self, url, dateindex=None, index_col=None, fill_col=None):
        """
        Initialize the main dataframe from csv data
        """
        try:
            self.df = self._load_csv(
                url, dateindex, index_col, fill_col)
        except Exception as e:
            self.err(e, self.load_csv, "Can not load csv file")

    def load_csv_(self, url, dateindex=None, index_col=None, fill_col=None):
        """
        Returns a DataSwim instance from csv data
        """
        try:
            df = self._load_csv(url, dateindex, index_col, fill_col)
            return self.clone_(df)
        except Exception as e:
            self.err(e, self.load_csv_, "Can not load csv file")

    def _load_csv(self, url, dateindex, index_col, fill_col):
        """
        Returns a DataSwim instance from csv data
        """

        try:
            df = pd.read_csv(url)
            ds2 = self.clone_(df=df)
        except FileNotFoundError as e:
            msg = "File " + url + " not found"
            self.warning(msg)
            return
        except Exception as e:
            self.err(e)
            return
        if dateindex is not None:
            ds2 = ds2.dateindex_(dateindex)
        if fill_col is not None:
            ds2 = ds2.fill_nan_(0, fill_col)
        if index_col is not None:
            ds2 = ds2.index_col_(index_col)
        return ds2.df
