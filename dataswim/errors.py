# -*- coding: utf-8 -*-

from __future__ import print_function
from goerr import err


class Errors():
    """
    Class to handle errors
    """

    def __init__(self, df=None, db=None):
        """
        Initialize with an empty dataframe
        """
        self.autoprint = True
        self.errors_handling = "exceptions"

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
        err.new(msg, func)
        if self.errors_handling == "trace":
            self.debug(str(len(err.errs)) + ".",
                       "An error has occured: use trace() to get the stack trace")
        else:
            self.trace()

    def trace(self):
        """
        Prints the error trace
        """
        if err.exists:
            print("")
            err.throw(reverse=True)

    def errs(self):
        """
        Sets the error handling mode to trace
        """
        self.errors_handling = "trace"
