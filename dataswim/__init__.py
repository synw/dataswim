# -*- coding: utf-8 -*-

import pandas as pd
from numpy import NaN, where
from goerr import err
from .db import Db
from .charts import Plot
from .data import Df
from .report import Report
from .errors import Errors
from .messages import Messages
from _ast import arg

__version__ = "0.2.2"


class DataSwim(Db, Df, Plot, Report, Errors, Messages):
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
        self.chart_opts = dict(width=940)
        self.chart_style = dict(color="blue")
        self.label = None
        self.reports = []
        self.report_path = None
        self.backup_df = None
        self.autoprint = True
        self.errors_handling = "exceptions"

    def __repr__(self):
        msg = "<DataSwim object>"
        return msg

    def new_(self, df=None, db=None):
        """
        Returns a new DataSwim instance from a dataframe
        """
        ds2 = DataSwim(df, db)
        if self.autoprint is True:
            self.ok("A new instance was created")
        return ds2


ds = DataSwim()
