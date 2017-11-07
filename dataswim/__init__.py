# -*- coding: utf-8 -*-

import pandas as pd
from numpy import NaN, where
from goerr import err
from .db import Db
from .charts import Plot
from .data import Df
from .report import Report


class DataSwim(Db, Df, Plot, Report):
    """
    Main class
    """

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df
        self.db = None
        self.x_field = None
        self.y_field = None
        self.chart_obj = None
        self.chart_opts = dict(width=940)
        self.chart_style = dict(color="blue")
        self.label = None
        self.reports = []
        self.report_path = None
        self.backup_df = None

    def new(self, df):
        """
        Returns a new instance from a dataframe
        """
        return DataSwim(df)


ds = DataSwim()
