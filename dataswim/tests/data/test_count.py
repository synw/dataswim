import pandas as pd
from dataswim.tests.base import BaseDsTest
from dataswim import ds

ds.errs_traceback = False


class TestDsDataCount(BaseDsTest):

    def test_count(self):
        ds.df = self.df
        msg = "Found 2 rows in the dataframe"
        self.assertPrintMsg("ok", msg, ds.count)
        num = ds.count_()
        self.assertEqual(num, 2)
        ds.df = None
        ds.count()
        self.assertRaises(AttributeError)
        ds.count_()
        self.assertRaises(AttributeError)

    def test_count_nulls(self):
        ds.df = pd.DataFrame({"one": None, "two": 2}, ["1", "2"])
        msg = "Found 2 nulls in column one"
        self.assertPrintMsg("ok", msg, ds.count_nulls, "one")
        ds.count_nulls("wrong")
        self.assertRaises(KeyError)
        ds.df = None
        ds.count_nulls("one")
        self.assertRaises(TypeError)

    def test_count_empty(self):
        ds.df = pd.DataFrame({"one": "", "two": 2}, ["1", "2"])
        msg = "Found 2 empty rows in column one"
        self.assertPrintMsg("ok", msg, ds.count_empty, "one")
        ds.count_empty("wrong")
        self.assertRaises(KeyError)
        ds.df = None
        ds.count_empty("one")
        self.assertRaises(TypeError)

    def test_count_zero(self):
        ds.df = pd.DataFrame({"one": 0, "two": 2}, ["1", "2"])
        msg = "Found 2 zero values in column one"
        self.assertPrintMsg("ok", msg, ds.count_zero, "one")
        ds.count_zero("wrong")
        self.assertRaises(KeyError)
        ds.df = None
        ds.count_zero("one")
        self.assertRaises(TypeError)

    def test_count_unique(self):
        ds.df = pd.DataFrame({"one": 0, "two": 2}, ["1", "2"])
        msg = "Found 1 unique values in column one"
        self.assertPrintMsg("ok", msg, ds.count_unique, "one")
        ds.count_unique("wrong")
        self.assertRaises(KeyError)
        ds.df = None
        ds.count_unique("one")
        self.assertRaises(TypeError)

