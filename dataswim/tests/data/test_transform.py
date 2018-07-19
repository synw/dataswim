# -*- coding: utf-8 -*-
import pandas as pd
from pandas.testing import assert_frame_equal
from dataswim.tests.base import BaseDsTest
from dataswim import ds

ds.errs_traceback = False


class TestDsDataTransform(BaseDsTest):

    def test_keep(self):
        df1 = pd.DataFrame([[1,2], [1,2]], columns = ["one", "two"])
        ds.df = df1
        ds.keep("one")
        df2 = pd.DataFrame([1,1], columns = ["one"])
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds2 = ds.keep_("one")
        assert_frame_equal(ds2.df, df2)
        ds.df = None
        self.assertErr("TypeError", ds.keep, "one")
        self.assertErr("TypeError", ds.keep_, "one")

    def test_rsum(self):
        df1 = pd.DataFrame([["2001/01/01", 1], ["2001/02/01", 5],
                            ["2001/02/15", 3], ["2001/02/28", 3]],
                            columns = ["date", "value"])
        ds.df = df1
        ds.rsum(time_period="1M", dateindex="date", index_col=None)
        index = pd.DatetimeIndex(["2001/01/31", "2001/02/28"], name="date")
        df2 = pd.DataFrame([[1, 1], [11, 3]], columns = ["value", "Number"],
                           index=index)
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds2 = ds.rsum_(time_period="1M", dateindex="date", index_col=None)
        assert_frame_equal(ds2.df, df2)
        ds.df = None
        self.assertErr(None, ds.rsum, time_period="1M",
                       dateindex="date")
        self.assertErr(None, ds.rsum_, time_period="1M",
                       dateindex="date")

    def test_rmean(self):
        df1 = pd.DataFrame([["2001/01/01", 1], ["2001/01/02", 2],
                            ["2001/02/15", 1], ["2001/02/28", 2]],
                            columns = ["date", "value"])
        ds.df = df1
        ds.rmean(time_period="1M", dateindex="date", index_col=None)
        index = pd.DatetimeIndex(["2001/01/31", "2001/02/28"], name="date")
        df2 = pd.DataFrame(pd.DataFrame([[1.5, 2], [1.5, 2]],
                  columns = ["value", "Number"], index=index))
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds2 = ds.rmean_(time_period="1M", dateindex="date", index_col=None)
        assert_frame_equal(ds2.df, df2)
        ds.df = None
        self.assertErr(None, ds.rmean, time_period="1M",
                       dateindex="date")
        self.assertErr(None, ds.rmean_, time_period="1M",
                       dateindex="date")

    def test_resample(self):
        df1 = pd.DataFrame([["2001/01/01", 1], ["2001/01/02", 2],
                            ["2001/02/15", 1], ["2001/02/28", 2]],
                            columns = ["date", "value"])
        ds.df = df1
        ds.dateindex("date")
        ds.df = ds._resample_(time_period="1M", method="sum", num_col=None,
                             fill_col=None, dateindex=None, index_col=None)
        index = pd.DatetimeIndex(["2001/01/31", "2001/02/28"], name="date")
        df2 = pd.DataFrame([[3], [3]], columns = ["value"], index=index)
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds.df = ds._resample_(time_period="1M", method="mean", num_col="num",
                             fill_col=None, dateindex=None, index_col=None)
        ds.df = df1
        self.assertErr(None, ds._resample_, time_period="1M",
                       method="sum", num_col=None, fill_col=None,
                       dateindex="wrong", index_col=None)
        self.assertErr(None, ds._resample_, time_period="1M",
                       method="wrong", num_col=None, fill_col=None,
                       dateindex="date", index_col=None)
        self.assertErr(None, ds._resample_, time_period="1M",
                       method="sum", num_col="n", fill_col="wrong",
                       dateindex="wrong", index_col=None)

    def test_drop(self):
        df1 = pd.DataFrame([[1,2], [1,2]], columns = ["one", "two"])
        ds.df = df1
        ds.drop("two")
        df2 = pd.DataFrame([1,1], columns = ["one"])
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        msg = "Column wrong not found. Aborting"
        self.assertWarning(msg, ds.drop, "wrong")
        ds.df = None
        self.assertErr("AttributeError", ds.drop, "wrong")

    def test_exclude(self):
        df1 = pd.DataFrame([[2,2], [1,2]], columns = ["one", "two"])
        ds.df = df1
        ds.exclude("one", 1)
        df2 = pd.DataFrame([[2, 2]], columns = ["one", "two"])
        assert_frame_equal(ds.df, df2)
        self.assertErr("KeyError", ds.exclude, "wrong", 0)
