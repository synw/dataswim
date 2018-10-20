# @PydevCodeAnalysisIgnore
import pandas as pd
import deepdish as dd
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

    def _duplicate_(self, df=None, db=None, quiet=True):
        try:
            if db is None:
                db = self.db
            if df is None:
                if self.df is None:
                    self.err("The main dataframe is empty and no dataframe"
                             " was provided: please provide a dataframe as argument")
                    return
                df = self.df.copy()
            ds2 = self.new_(df, db, True)
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
            ds2.quiet = self.quiet
        except Exception as e:
            self.err(e, "Can not duplicate instance")
            return
        if quiet is False:
            self.ok("A duplicated instance was created")
        return ds2

    def clone_(self, quiet=False):
        """
        Clone the DataSwim instance
        """
        ds2 = self._duplicate_(quiet=True)
        if ds2 is None:
            self.err("Can not clone instance")
        else:
            if quiet is False:
                self.ok("Instance cloned")
        return ds2

    def backup(self):
        """
        Backup the main dataframe
        """
        try:
            self.backup_df = self.df.copy()
        except Exception as e:
            self.err(e, "Can not backup data")
            return
        self.ok("Dataframe backed up")

    def restore(self):
        """
        Restore the main dataframe
        """
        if self.backup_df is None:
            self.warning("No dataframe is backed up: nothing restore")
            return
        self.df = self.backup_df
        self.ok("Dataframe is restored")

    def load_json(self, path, **kwargs):
        """
        Load data in the main dataframe from json
        """
        try:
            df = pd.read_json(path, **kwargs)
            self.df = df
        except Exception as e:
            self.err(e, "Can not load json")

    def load_h5(self, filepath):
        """
        Load a Hdf5 file to the main dataframe
        """
        try:
            self.start("Loading Hdf5 data...")
            self.df = dd.io.load(filepath)
            self.end("Finished loading Hdf5 data")
        except Exception as e:
            self.err(e, "Can not load Hdf5 file")

    def load_excel(self, filepath, **kwargs):
        """
        Set the main dataframe with the content of an Excel file
        """
        try:
            df = pd.read_excel(filepath, **kwargs)
            if len(df.index) == 0:
                self.warning("Empty Excel file. Can not set the dataframe.")
                return
            self.df = df
        except Exception as e:
            self.err(e, "Can not load Excel file")

    def load_csv(self, url, dateindex=None,
                 index_col=None, fill_col=None, num_col=None, **kwargs):
        """
        Loads csv data in the main dataframe
        """
        self.start("Loading csv...")
        try:
            if self.datapath is not None and url.startswith("/") is False:
                url = self.datapath + "/" + url
            df = pd.read_csv(url, **kwargs)
            self.df = df
        except FileNotFoundError:
            msg = "File " + url + " not found"
            self.warning(msg)
            return
        except Exception as e:
            self.err(e, "Can not load csv file")
            return
        ds2 = self.transform_(dateindex, index_col, fill_col, df=self.df)
        if ds2 is None:
            self.err("Can not load csv")
            return
        self = ds2
        self.end("Finished loading csv")

    def dateparser(self, dformat='%d/%m/%Y'):
        """
        Returns a date parser for pandas
        """

        def dateparse(dates):
            return [pd.datetime.strptime(d, dformat) for d in dates]

        return dateparse
