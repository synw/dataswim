# -*- coding: utf-8 -*-
import datetime
import pandas as pd
import numpy as np
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
        self.assertErr("TypeError", ds.drop_nan, "one")

    def test_zero_nan(self):
        df1 = pd.DataFrame({"one": ["one","two"], "two":
            ["two", 0]}, ["1", "2"])
        ds.df = df1
        ds.zero_nan("two")
        df2 = pd.DataFrame({"one": ["one", "two"], "two":
                ["two", nan]}, ["1", "2"])
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds2 = ds.zero_nan_("two")
        assert_frame_equal(ds2.df, df2)
        ds.zero_nan("two", "one")
        ds.df = None
        self.assertErr("AttributeError", ds.zero_nan, "one", "two")
        ds.df = df1
        msg = "Column wrong does not exist"
        self.assertWarning(msg, ds.zero_nan, "wrong", "two")
        self.assertErr(None, ds.zero_nan, "wrong", "wrong")
        self.assertWarning(msg, ds.zero_nan_, "wrong", "two")
        self.assertErr(None, ds.zero_nan_, "wrong", "wrong")

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
        self.assertErr("AttributeError", ds.fill_nan, "val", "two")
        self.assertErr("AttributeError", ds.fill_nan_, "val", "two")
        ds.df = df1
        msg = "Can not find column wrong"
        self.assertWarning(msg, ds.fill_nan, "val", "wrong")
        self.assertErr(None, ds.fill_nan, "val", "wrong")

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
        self.assertErr("AttributeError", ds.replace, "one", "two", "three")
        self.assertErr("AttributeError", ds.replace_, "one", "two", "three")

    def test_to_int(self):
        df1 = pd.DataFrame({"one": ["one", "two"], "two":
                            [1.0, 2.0]}, ["1", "2"])
        ds.df = df1
        ds.to_int("two")
        self.assertEqual(list(ds.df["two"]), [1, 2])
        ds.df = None
        self.assertErr("TypeError", ds.to_int, "two")
        ds.df = pd.DataFrame({"one": ["one", "two"], "two":
                            ["wrong", 2.0]}, ["1", "2"])
        self.assertErr("ValueError", ds.to_int, "two")

    def test_to_float(self):
        df1 = pd.DataFrame({"one": ["one", "two"], "two":
                            [1, 2]}, ["1", "2"])
        ds.df = df1
        ds.to_float("two")
        self.assertEqual(list(ds.df["two"]), [1.0, 2.0])
        ds.df = None
        self.assertErr("AttributeError", ds.to_float, "two")
        ds.df = pd.DataFrame({"one": ["one", "two"], "two":
                            ["wrong", 2]}, ["1", "2"])
        self.assertErr("ValueError", ds.to_float, "two")

    def test_to_type(self):
        df1 = pd.DataFrame({"one": ["one", "two"], "two":
                            [1, 2]}, ["1", "2"])
        ds.df = df1
        df = ds.to_type("float64", "two")
        df2 = pd.DataFrame({"one": ["one", "two"], "two":
                            [1.0, 2.0]}, ["1", "2"])
        assert_frame_equal(df, df2)
        ds.df = None
        self.assertErr("AttributeError", ds.to_type, "float64", "two")
        ds.df = pd.DataFrame({"one": ["one", "two"], "two":
                            ["wrong", 2.0]}, ["1", "2"])
        self.assertErr(None, ds.to_type, "float64", "two")
        self.assertErr(None, ds.to_type, "float64", "wrong")

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

    def test_date_index(self):
        df1 = pd.DataFrame({"one": ["one","two"], "date":
            ["2002/12/01", "2002/12/02"]}, [1, 2])
        ds.df = df1
        ds.dateindex("date")
        index = np.array(['2002-12-01T00:00:00.000000000',
                       '2002-12-02T00:00:00.000000000'],
                        dtype="datetime64[ns]")
        np.testing.assert_array_equal(ds.df.index.values, index)
        ds.df = df1
        ds2 = ds.dateindex_("date")
        np.testing.assert_array_equal(ds2.df.index.values, index)
        ds.df = None
        ds.dateindex_("date")
        self.assertRaises(TypeError)
        ds.dateindex("date")
        self.assertRaises(TypeError)
        ds.dateindex("wrong")
        self.assertRaises(TypeError)

    def test_index(self):
        df1 = pd.DataFrame([[1, 3], [2, 4]], columns=["one", "two"])
        ds.df = df1
        ds.index("one")
        index = np.array([1, 2])
        np.testing.assert_array_equal(ds.df.index.values, index)
        ds.df = df1
        ds2 = ds.index_("one")
        np.testing.assert_array_equal(ds2.df.index.values, index)
        ds.df = None
        ds.index("one")
        self.assertRaises(TypeError)
        ds.index_("one")
        self.assertRaises(TypeError)

    def test_strip(self):
        df1 = pd.DataFrame([[" whitespace ", 3], [2, 4]],
                           index=["one", "two"])
        ds.df = df1
        ds.strip("one")
        df2 = pd.DataFrame([["whitespace", 3], [2, 4]],
                           index=["one", "two"])
        assert_frame_equal(ds.df, df2)
        ds.df = None
        ds.strip("one")
        self.assertRaises(TypeError)
        ds.df = "wrong"
        ds.index("one")
        self.assertRaises(AttributeError)

    def test_strip_cols(self):
        df1 = pd.DataFrame([[1, 3], [2, 4]],
                           columns=[" one ", " two "])
        ds.df = df1
        ds.strip_cols()
        df2 = pd.DataFrame([[1, 3], [2, 4]],
                           columns=["one", "two"])
        assert_frame_equal(ds.df, df2)
        ds.df = pd.DataFrame([[1, 3], [2, 4]],
                           columns=["one", None])
        ds.strip_cols()

    def test_roundvals(self):
        df1 = pd.DataFrame([[1.345854, 3.0], [2.1, 4.0]],
                           columns=["one", "two"])
        ds.df = df1
        ds.roundvals("one")
        df2 = pd.DataFrame([[1.35, 3.0], [2.1, 4.0]],
                           columns=["one", "two"])
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds.roundvals("wrong")
        self.assertRaises(KeyError)

    def test_format_date(self):
        date = datetime.datetime(2011, 1, 3, 0, 0)
        d2 = ds.format_date_(date)
        self.assertEqual(d2, '2011-01-03 00:00:00')

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

