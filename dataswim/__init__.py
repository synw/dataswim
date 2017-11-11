# -*- coding: utf-8 -*-

import pandas as pd
from numpy import NaN, where
from goerr import err
from .db import Db
from .charts import Plot
from .data import Df
from .report import Report
from goerr.colors import cols
from _ast import arg

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

    def new(self, df=None, db=None):
        """
        Returns a new DataSwim instance from a dataframe
        """
        return DataSwim(df, db)

    def duplicate(self, df=None, db=None):
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
        ex = None
        msg = None
        func = None
        for arg in args:
            if isinstance(arg, Exception):
                ex = arg
            elif isinstance(arg, str):
                msg = arg
            elif callable(arg) is True:
                func = arg
        if ex is not None:
            err.new(ex)
            if len(args) < 3:
                return
        if func is None or msg is None:
            f = ""
            if func is not None:
                f = "(from function " + str(func) + ")"
            err.new(
                "Please provide a function and a message to the error constructor " + f)
            err.throw()
        err.new(msg, func)
        if self.errors_handling == "trace":
            print(str(len(err.errs)) + ".",
                  "An error has occured: use ds.trace() to get the stack trace")
        else:
            self.trace()

    def trace(self):
        """
        Prints the error trace
        """
        if err.exists:
            print("")
            err.throw(reverse=True)

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

    def errs(self):
        """
        Sets the error handling mode to trace
        """
        self.errors_handling = "trace"


ds = DataSwim()
