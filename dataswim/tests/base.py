import os
import unittest
from io import StringIO
from contextlib import redirect_stdout
import pandas as pd
from goerr.colors import colors
from goerr.testing import assert_err
from dataswim import ds


class BaseDsTest(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({"one": 1, "two": 2}, ["1", "2"])
        self.path = os.path.dirname(os.path.realpath(__file__))

    def debug(self, *elements):
        print("-------------------------------------------")
        ds.debug(*elements)
        print("-------------------------------------------")

    def assertErr(self, err_type, func, *args, **kwargs):
        assert_err(err_type, func, *args, **kwargs)

    def assertWarning(self, txt, func, *args, **kwargs):
        self._assertPrintMsg(True, "warning", txt, func, *args, **kwargs)

    def assertOk(self, txt, func, *args, **kwargs):
        self._assertPrintMsg(False, "ok", txt, func, *args, **kwargs)

    def _assertPrint(self, contains, expected, func, *args, **kwargs):
        f = StringIO()
        with redirect_stdout(f):
            func(*args, **kwargs)
        displayed = f.getvalue()
        if contains is True:
            self.assertIn(expected, displayed)
        else:
            self.assertEqual(displayed, expected)

    def _assertPrintMsg(self, contains, msg_class, txt, func, *args, **kwargs):
        if msg_class == "ok":
            label = colors.green("OK")
        elif msg_class == "warning":
            label = colors.yellow("WARNING")
        elif msg_class == "info":
            label = colors.blue("INFO")
        elif msg_class == "progress":
            label = colors.purple("Progress")
        elif msg_class == "start":
            label = colors.purple("START")
        elif msg_class == "end":
            label = colors.purple("END")
        expected = ds.msg_(label, txt)+"\n"
        self._assertPrint(contains, expected, func, *args, **kwargs)
