# -*- coding: utf-8 -*-
import pandas as pd
from numpy import nan
from pandas.testing import assert_frame_equal
from dataswim.tests.base import BaseDsTest
from dataswim import ds

ds.errs_traceback = False


class TestDsDataClean(BaseDsTest):

    def test_drop_nan(self):
        df1 = pd.DataFrame({"one": ["one","two"], "two":
            ["two", None]}, ["1", "2"])
        ds.df = df1
        ds.drop_nan("two")
        df2 = pd.DataFrame({"one": "one", "two": "two"}, ["1"])
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds.drop_nan(method="any")
        assert_frame_equal(ds.df, df2)
        ds.df = None
        ds.drop_nan()
        self.assertRaises(AttributeError)

    def test_zero_nan(self):
        df1 = pd.DataFrame({"one": ["one","two"], "two":
            ["two", 0]}, ["1", "2"])
        ds.df = df1
        ds.zero_nan("two")
        df2 = pd.DataFrame({"one": ["one","two"], "two":
            ["two", nan]}, ["1", "2"])
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds2 = ds.zero_nan_("two")
        assert_frame_equal(ds2.df, df2)
        ds.zero_nan("two", "one")
        ds.df = None
        ds.zero_nan("two")
        self.assertRaises(AttributeError)
        ds.df = df1
        ds.zero_nan("wrong", "wrong")
        ds.zero_nan_("wrong", "wrong")

    def test_fill_nan(self):
        df1 = pd.DataFrame({"one": ["one", "two"], "two":
                            ["two", None]}, ["1", "2"])
        ds.df = df1
        ds.fill_nan("two", "two")
        df2 = pd.DataFrame({"one": ["one", "two"], "two":
                            ["two", "two"]}, ["1", "2"])
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds.fill_nan("two")
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds2 = ds.fill_nan_("two", "two")
        assert_frame_equal(ds2.df, df2)
        ds.df = None
        ds.fill_nan("two", "two")
        ds.fill_nan_("two", "two")
        self.assertRaises(AttributeError)
        ds.df = df1
        ds.fill_nan("two", "wrong")
        self.assertRaises(KeyError)

    def test_replace(self):
        df1 = pd.DataFrame({"one": ["one", "two"], "two":
                            ["two", "two"]}, ["1", "2"])
        ds.df = df1
        ds.replace("one", "two", "three")
        df2 = pd.DataFrame({"one": ["one", "three"], "two":
                            ["two", "two"]}, ["1", "2"])
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds2 = ds.replace_("one", "two", "three")
        assert_frame_equal(ds2.df, df2)
        ds.df = None
        ds.replace_("one", "two", "three")
        self.assertRaises(AttributeError)
        ds.replace("one", "two", "three")
        self.assertRaises(AttributeError)

    def test_to_int(self):
        df1 = pd.DataFrame({"one": ["one", "two"], "two":
                            [1.0, 2.0]}, ["1", "2"])
        ds.df = df1
        ds.to_int("two")
        df2 = pd.DataFrame({"one": ["one", "two"], "two":
                            [1, 2]}, ["1", "2"])
        assert_frame_equal(ds.df, df2)
        ds.df = None
        ds.to_int("two")
        self.assertRaises(AttributeError)
        ds.df = pd.DataFrame({"one": ["one", "two"], "two":
                            ["wrong", 2.0]}, ["1", "2"])
        self.assertRaises(ValueError)

    def test_to_float(self):
        df1 = pd.DataFrame({"one": ["one", "two"], "two":
                            [1, 2]}, ["1", "2"])
        ds.df = df1
        ds.to_float("two")
        df2 = pd.DataFrame({"one": ["one", "two"], "two":
                            [1.0, 2.0]}, ["1", "2"])
        assert_frame_equal(ds.df, df2)
        ds.df = None
        ds.to_float("two")
        self.assertRaises(AttributeError)
        ds.df = pd.DataFrame({"one": ["one", "two"], "two":
                            ["wrong", 2]}, ["1", "2"])
        self.assertRaises(ValueError)

    def test_to_type(self):
        df1 = pd.DataFrame({"one": ["one", "two"], "two":
                            [1, 2]}, ["1", "2"])
        ds.df = df1
        df = ds.to_type("float64", "two")
        df2 = pd.DataFrame({"one": ["one", "two"], "two":
                            [1.0, 2.0]}, ["1", "2"])
        assert_frame_equal(df, df2)
        ds.df = None
        df = ds.to_type("float64", "two")
        self.assertRaises(AttributeError)
        ds.df = pd.DataFrame({"one": ["one", "two"], "two":
                            ["wrong", 2.0]}, ["1", "2"])
        self.assertRaises(ValueError)
        df = ds.to_type(float, "wrong")
        self.assertRaises(AttributeError)

    def tests_timestamps(self):
        df1 = pd.DataFrame({"one": ["one","two"], "two":
            ["2002/12/01", "2002/12/02"]}, [1, 2])
        ds.df = df1
        ds.timestamps("two",name= "ts")
        df2 = pd.DataFrame({"one": ["one","two"], "ts": [1038700800,
            1038787200], "two":
            ["2002/12/01", "2002/12/02"]}, [1, 2])
        ds.df = ds.df.reindex(sorted(ds.df.columns), axis=1)
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds.timestamps("two")
        ds.timestamps("two", unit="s", errors="raise")
        ds.df = None
        ds.timestamps("two")
        self.assertRaises(AttributeError)

    def test_dates(self):
        ds.df = pd.DataFrame({"one": ["one","two"], "two":
            ["2002/12/01", "2003/12/02"]}, [1, 2])
        ds.date("two")
        df2 = pd.DataFrame({"one": ["one","two"],"two":
            ["2002-12-01 00:00:00", "2003-12-02 00:00:00"]}, [1, 2])
        assert_frame_equal(ds.df, df2)

        ds.df = pd.DataFrame({"one": ["one","two"], "two":
            ["2002/12/01", "2003/12/02"]}, [1, 2])
        df2 = pd.DataFrame({"one": ["one","two"],"two":
            ["2002", "2003"]}, [1, 2])
        ds.date("two", precision="Y")
        assert_frame_equal(ds.df, df2)

        ds.df = pd.DataFrame({"one": ["one","two"], "two":
            ["2002/12/01", "2003/12/02"]}, [1, 2])
        df2 = pd.DataFrame({"one": ["one","two"],"two":
            ["2002-12", "2003-12"]}, [1, 2])
        ds.date("two", precision="M")
        assert_frame_equal(ds.df, df2)

        ds.df = pd.DataFrame({"one": ["one","two"], "two":
            ["2002/12/01", "2003/12/02"]}, [1, 2])
        df2 = pd.DataFrame({"one": ["one","two"],"two":
            ["2002-12-01", "2003-12-02"]}, [1, 2])
        ds.date("two", precision="D")
        assert_frame_equal(ds.df, df2)

        ds.df = pd.DataFrame({"one": ["one","two"], "two":
            ["2002/12/01", "2003/12/02"]}, [1, 2])
        df2 = pd.DataFrame({"one": ["one","two"],"two":
            ["2002-12-01 00", "2003-12-02 00"]}, [1, 2])
        ds.date("two", precision="H")
        assert_frame_equal(ds.df, df2)

        ds.df = pd.DataFrame({"one": ["one","two"], "two":
            ["2002/12/01", "2003/12/02"]}, [1, 2])
        df2 = pd.DataFrame({"one": ["one","two"],"two":
            ["2002-12-01 00:00", "2003-12-02 00:00"]}, [1, 2])
        ds.date("two", precision="Min")
        assert_frame_equal(ds.df, df2)

        ds.df = pd.DataFrame({"one": ["one","two"], "two":
            ["2002/12/01", "2003/12/02"]}, [1, 2])
        ds.date("wrong")
        self.assertRaises(KeyError)

        ds.df = pd.DataFrame({"one": ["one","two"], "two":
            ["2002/12/01", "wrong"]}, [1, 2])
        ds.date("two", "wrong")
        self.assertRaises(TypeError)

        ds.df = None
        ds.date("two")
        self.assertRaises(ValueError)

    def test_nulls(self):
        df1 = pd.DataFrame({"one": ["one", "two"], "two":
                            ["", None]}, ["1", "2"])
        ds.df = df1
        ds.fill_nulls("two")
        df2 = pd.DataFrame({"one": ["one", "two"], "two":
                            [nan, nan]}, ["1", "2"])
        assert_frame_equal(ds.df, df2)
        ds.df = None
        ds.fill_nulls("two")
        self.assertRaises(AttributeError)


    def test_nan_empty(self):
        df1 = pd.DataFrame({"one": ["one","two"], "two":
            ["two", ""]}, ["1", "2"])
        ds.df = df1
        ds.nan_empty("two")
        df2 = pd.DataFrame({"one": ["one","two"], "two":
            ["two", nan]}, ["1", "2"])
        assert_frame_equal(ds.df, df2)
        ds.df = None
        ds.nan_empty("two")
        self.assertRaises(TypeError)

