# -*- coding: utf-8 -*-

import pandas as pd
from numpy import NaN, where
from goerr import err
from .db import Db
from .charts import Plot
from .data import Df


class DataSwim(Plot, Db, Df):
    """
    Main class
    """
    pass

    def new(self, df):
        """
        Returns a new instance of self.new from a dataframe
        """
        return DataSwim(df)


ds = DataSwim()
