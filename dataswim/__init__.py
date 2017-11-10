# -*- coding: utf-8 -*-

import pandas as pd
from numpy import NaN, where
from goerr import err
from .db import Db
from .charts import Plot
from .data import Df
from .report import Report
from goerr.colors import cols

__version__ = "0.2.2"


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
        self.autoprint = True
        self.errors_handling = "exceptions"

    def __repr__(self):
        msg = "<DataSwim object>"
        return msg

    def new(self, df=None, db=None):
        """
        Returns a new DataSwim instance from a dataframe
        """
        return DataSwim(df, db)

    def duplicate(self, db=None, df=None):
        """
        Returns a new DataSwim instance using the previous database connection
        """
        if db is None:
            db = self.db
        if df is None:
            df = self.df.copy()
        return DataSwim(db=db, df=df)

    def clone(self):
        """
        Returns a new DataSwim instance from the current instance
        """
        return DataSwim(self.df, self.db)

    def ok(self, *msg):
        """
        Returns a message with an ok prefix
        """
        li = []
        for el in msg:
            li.append(str(el))
        txt = " ".join(li)
        res = "[" + cols.SUCCESS + "ok" + cols.ENDC + "] " + txt
        print(res)

    def err(self, *args):
        """
        Error handling
        """
        err.new(*args)
        if self.errors_handling == "trace":
            print(str(len(err.errs)) + ".",
                  "An error has occured: use ds.trace() to get the stack trace")
        else:
            err.throw()

    def trace(self):
        """
        Prints the error trace
        """
        if err is not None:
            err.throw()
        else:
            print("No errors")

    def warning(self, msg):
        """
        Prints a warning
        """
        print("[" + cols.WARNING + "WARNING" + "]" + cols.ENDC + " " + msg)

    def debug(self, msg):
        """
        Prints a warning
        """
        print("[" + cols.WARNING + "DEBUG" + "]" + cols.ENDC + " " + msg)

    def fatal(self, *args):
        """
        Prints the error trace
        """
        if len(args) > 0:
            err.new(*args)
            err.throw()
        else:
            print("No errors")

    def errs(self):
        """
        Sets the error handling mode to trace
        """
        self.errors_handling = "trace"


ds = DataSwim()
