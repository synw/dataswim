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
from .copy import Copy
from ..errors import Error
from ..messages import Message


class Df(Select, View, Transform, Clean, Count,
         Export, Search, Stats, Text, Copy):
    """
    Class for manipulating dataframes
    """

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
        """Load data in the main dataframe from json

        :param filepath: url of the csv file to load,
                                         can be absolute if it starts with ``/``
                                         or relative if it starts with ``./``
        :type filepath: str

        :param kwargs: keyword arguments to pass to
                                                   Pandas ``read_json`` function

        :example: ``ds.load_json("./myfile.json")``
        """
        try:
            df = pd.read_json(path, **kwargs)
            self.df = df
        except Exception as e:
            self.err(e, "Can not load json")

    def load_h5(self, filepath):
        """Load a Hdf5 file to the main dataframe

        :param filepath: url of the csv file to load,
                                         can be absolute if it starts with ``/``
                                         or relative if it starts with ``./``
        :type filepath: str

        :example: ``ds.load_h5("./myfile.hdf5")``
        """
        try:
            self.start("Loading Hdf5 data...")
            self.df = dd.io.load(filepath)
            self.end("Finished loading Hdf5 data")
        except Exception as e:
            self.err(e, "Can not load Hdf5 file")

    def load_excel(self, filepath, **kwargs):
        """Set the main dataframe with the content of an Excel file

        :param filepath: url of the csv file to load,
                        can be absolute if it starts with ``/``
                        or relative if it starts with ``./``
        :type filepath: str

        :param kwargs: keyword arguments to pass to 
                            Pandas ``read_excel`` function

        :example: ``ds.load_excel("./myfile.xlsx")``
        """
        try:
            df = pd.read_excel(filepath, **kwargs)
            if len(df.index) == 0:
                self.warning("Empty Excel file. Can not set the dataframe.")
                return
            self.df = df
        except Exception as e:
            self.err(e, "Can not load Excel file")

    def load_csv(self, url, **kwargs):
        """Loads csv data in the main dataframe

        :param url: url of the csv file to load:
                                can be absolute if it starts with ``/``
                                or relative if it starts with ``./``
        :type url: str
        :param kwargs: keyword arguments to pass to Pandas
                                    ``read_csv`` function

        :example: ``ds.load_csv("./myfile.csv")``
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
        self.end("Finished loading csv")

    def dateparser(self, dformat='%d/%m/%Y'):
        """
        Returns a date parser for pandas
        """

        def dateparse(dates):
            return [pd.datetime.strptime(d, dformat) for d in dates]

        return dateparse
