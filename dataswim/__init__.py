# -*- coding: utf-8 -*-

import pandas as pd
from numpy import NaN, where
from goerr import err
from .db import Db
from .charts import Plot
from .data import Df


class DataSwim(Db, Df, Plot):
    """
    Main class
    """

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df

    def new(self, df):
        """
        Returns a new instance from a dataframe
        """
        return DataSwim(df)


ds = DataSwim()
