# -*- coding: utf-8 -*-

import pandas as pd
from numpy import NaN, where
from goerr import err
from .db import Db
from .charts import Plot
from .data import Df
from .report import Report

__version__ = "0.2.3"


class DataSwim(Db, Df, Plot, Report):
    """
    Main class
    """

    def __init__(self, df=None, db=None):
        """
        Initialize with an empty dataframe
        """
        global __version__
        self.version = __version__
        self.df = df
        self.db = db
        self.x_field = None
        self.y_field = None
        self.chart_obj = None
        self.opts = dict(width=940)
        self.style = dict(color="blue")
        self.label = None
        self.reports = []
        self.report_path = None
        self.backup_df = None

    def new(self, df=None, db=None):
        """
        Returns a new DataSwim instance from a dataframe
        """
        return DataSwim(df, db)

    def duplicate(self):
        """
        Returns a new DataSwim instance using the previous database connection
        """
        return DataSwim(db=self.db)

    def clone(self):
        """
        Returns a new DataSwim instance from the current instance
        """
        return DataSwim(self.df, self.db)


ds = DataSwim()
