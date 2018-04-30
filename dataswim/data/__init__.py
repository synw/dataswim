# -*- coding: utf-8 -*-

import pandas as pd
import deepdish as dd
from goerr import err
from .views import View
from .clean import Clean
from .count import Count
from .select import Select
from .transform import Transform
from .export import Export
from .search import Search
from .stats import Stats
from .text import Text


class Df(Select, View, Transform, Clean, Count, Export, Search, Stats, Text):
    """
    Class for manipulating dataframes
    """

    def duplicate_(self, df=None, db=None, quiet=False):
        """
        Returns a new DataSwim instance using the previous database connection
        """
        try:
            if db is None:
                db = self.db
            if df is None:
                if self.df is None:
                    self.err(
                        self.duplicate_, "The main dataframe is empty and no dataframe"
                        " was provided: please provide a dataframe as argument")
                    return
                df = self.df.copy()
            ds2 = self.new_(df, quiet=True)
            ds2.db = self.db
            ds2.x = self.x
            ds2.y = self.y
            ds2.chart_obj = self.chart_obj
            ds2.chart_opts = self.chart_opts
            ds2.chart_style = self.chart_style
            ds2.label = self.label
            ds2.reports = self.reports
            ds2.report_engines = self.report_engines
            ds2.backup_df = self.backup_df
            ds2.autoprint = self.autoprint
            ds2.errors_handling = self.errors_handling
            ds2.datapath = self.datapath
            ds2.report_path = self.report_path
            ds2.static_path = self.static_path
        except Exception as e:
            self.err(e, self.duplicate_, "Can not duplicate instance")
            return
        if self.autoprint is True and quiet is False:
            self.ok("A duplicated instance was created")
        return ds2

    def clone_(self, df=None, db=None):
        """
        Silently clone the DataSwim instance
        """
        try:
            ds2 = self.duplicate_(df, db, quiet=True)
            return ds2
        except Exception as e:
            self.err(e, self.clone_, "Can not clone instance")

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

    def load_data(self, dataset):
        """
        Set the main dataframe with the input data
        """
        try:
            df = self._load_data(dataset)
            self.df = df
        except Exception as e:
            err.new(e, self.load_data, "Can not load dataset")

    def load_data_(self, dataset):
        """
        Returns an instance with the input data
        """
        try:
            df = self._load_data(dataset)
            return self.clone_(df)
        except Exception as e:
            err.new(e, self._load_data, "Can not load dataset")

    def _load_data(self, dataset):
        """
        Convert the input data to pandas dataframe
        """
        df = pd.DataFrame()
        try:
            if isinstance(dataset, pd.DataFrame):
                return dataset
            elif isinstance(dataset, dict):
                df = self._dict_to_df(dataset)
            elif isinstance(dataset, list):
                return pd.DataFrame(dataset)
            else:
                err.new(self._load_data,
                        "Data format unknown: "
                        + str(type(dataset)) +
                        " please provide a dictionnary, a list or a Pandas DataFrame")
        except Exception as e:
            err.new(e, self._load_data, "Can not convert dataset")
        if err.exists:
            err.throw()
        return df

    def _dict_to_df(self, dictobj):
        """
        Converts a dictionary to a pandas dataframe
        """
        x = []
        y = []
        for datapoint in dictobj:
            x.append(datapoint)
            y.append(dictobj[datapoint])
        df = pd.DataFrame(dictobj)
        return df

    def load_json(self, path, **kwargs):
        """
        Load data in the main dataframe from json
        """
        try:
            df = pd.read_json(path, **kwargs)
            self.set(df)
        except Exception as e:
            self.err(e, self.load_excel, "Can not load json")

    def load_h5(self, filepath):
        """
        Load a Hdf5 file to the main dataframe
        """
        try:
            if self.autoprint is True:
                self.start("Loading Hdf5 data...")
            ds2 = self.clone_()
            ds2.df = dd.io.load(filepath)
            self = ds2
            if self.autoprint is True:
                self.end("Finished loading Hdf5 data...")
        except Exception as e:
            self.err(e, self.load_excel, "Can not load Hdf5 file")

    def load_excel(self, filepath, **kwargs):
        """
        Set the main dataframe with the content of an Excel file
        """
        try:
            df = self._load_excel(filepath, **kwargs)
            self.set(df)
        except Exception as e:
            self.err(e, self.load_excel, "Can not load Excel file")

    def _load_excel(self, filepath, **kwargs):
        """
        Set the main dataframe with the content of an Excel file
        """
        try:
            df = pd.read_excel(filepath, **kwargs)
            if df is None:
                self.warning("Empty Excel file. Can not set the dataframe.")
            return df
        except Exception as e:
            self.err(e, self._load_excel, "Can not load Excel file")

    def load_csv(self, url, dateindex=None,
                 index_col=None, fill_col=None, **kwargs):
        """
        Initialize the main dataframe from csv data
        """
        try:
            self.df = self._load_csv(
                url, dateindex, index_col, fill_col, **kwargs)
        except Exception as e:
            self.err(e, self.load_csv, "Can not load csv file")

    def load_csv_(self, url, dateindex=None,
                  index_col=None, fill_col=None, **kwargs):
        """
        Returns a DataSwim instance from csv data
        """
        try:
            df = self._load_csv(url, dateindex, index_col, fill_col, **kwargs)
            return self.clone_(df)
        except Exception as e:
            self.err(e, self.load_csv_, "Can not load csv file")

    def _load_csv(self, url, dateindex, index_col, fill_col, **kwargs):
        """
        Returns a DataSwim instance from csv data
        """
        if self.autoprint is True:
            self.start("Loading csv...")
        try:
            if self.datapath is not None and url.startswith("/") is False:
                url = self.datapath + "/" + url
            df = pd.read_csv(url, **kwargs)
            ds2 = self.clone_(df=df)
        except FileNotFoundError as e:
            msg = "File " + url + " not found"
            self.warning(msg)
            return
        except Exception as e:
            self.err(e, self._load_csv, "Can not load csv file")
            return
        try:
            ds2 = self.transform_(dateindex, index_col, fill_col, df=df)
        except Exception as e:
            self.err(e)
            return
        if self.autoprint is True:
            self.end("Finished loading csv")
        return ds2.df

    def dateparser(self, dformat='%d/%m/%Y'):
        """
        Returns a date parser for pandas
        """
        try:
            def dateparse(dates): return [
                pd.datetime.strptime(d, dformat) for d in dates]
            return dateparse
        except Exception as e:
            self.err(e, self.dateparser, "Can not create date parser")
