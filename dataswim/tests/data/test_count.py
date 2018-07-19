import pandas as pd
from dataswim.tests.base import BaseDsTest
from dataswim import ds

ds.errs_traceback = False


class TestDsDataCount(BaseDsTest):

    def test_count(self):
        ds.df = self.df
        msg = "Found 2 rows in the dataframe"
        self.assertOk(msg, ds.count)
        num = ds.count_()
        self.assertEqual(num, 2)
        ds.df = None
        self.assertErr("AttributeError", ds.count)
        self.assertErr("AttributeError", ds.count_)

    def test_count_nulls(self):
        ds.df = pd.DataFrame({"one": None, "two": 2}, ["1", "2"])
        msg = "Found 2 nulls in column one"
        self.assertOk(msg, ds.count_nulls, "one")
        msg = "Can not find column wrong"
        self.assertWarning(msg, ds.count_nulls, "wrong")
        ds.df = None
        self.assertErr("TypeError", ds.count_nulls, "one")

    def test_count_empty(self):
        ds.df = pd.DataFrame({"one": "", "two": 2}, ["1", "2"])
        msg = "Found 2 empty rows in column one"
        self.assertOk(msg, ds.count_empty, "one")
        self.assertErr("KeyError", ds.count_empty, "wrong")
        ds.df = None
        self.assertErr("TypeError", ds.count_empty, "one")

    def test_count_zero(self):
        ds.df = pd.DataFrame({"one": 0, "two": 2}, ["1", "2"])
        msg = "Found 2 zero values in column one"
        self.assertOk(msg, ds.count_zero, "one")
        self.assertErr("KeyError", ds.count_zero, "wrong")
        ds.df = None
        self.assertErr("TypeError", ds.count_zero, "one")

    def test_count_unique(self):
        ds.df = pd.DataFrame({"one": 0, "two": 2}, ["1", "2"])
        msg = "Found 1 unique values in column one"
        self.assertOk(msg, ds.count_unique, "one")
        self.assertErr("KeyError", ds.count_unique, "wrong")
        ds.df = None
        self.assertErr("TypeError", ds.count_unique, "one")
