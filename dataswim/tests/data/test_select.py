# -*- coding: utf-8 -*-
import pandas as pd
# import datetime
# import numpy as np
from pandas.testing import assert_series_equal, assert_frame_equal
from dataswim.tests.base import BaseDsTest
from dataswim import Ds

ds = Ds()
ds.errs_traceback = False


class TestDsDataSelect(BaseDsTest):

    def test_first(self):
        df1 = pd.DataFrame([["one", "three"], ["two", "four"]])
        ds.df = df1
        first = ds.first_()
        res = pd.Series(["one", "three"], name=0)
        assert_series_equal(first, res)
        ds.df = None
        ds.first_()
        self.assertRaises(AttributeError)

    def test_unique(self):
        df1 = pd.DataFrame([["one", "one", "three"], ["two", "two", "four"]])
        ds.df = df1
        data = ds.unique_(0)
        res = ["one", "two"]
        self.assertEqual(data, res)
        ds.df = None
        ds.unique_(0)
        self.assertRaises(AttributeError)

    def test_wunique(self):
        df1 = pd.DataFrame(
            {"col": ["one", "one", "two", "two", "two", "three"]})
        ds.df = df1
        df = ds.wunique_("col")
        df2 = pd.DataFrame({"Number": [3, 2, 1]}, ["two", "one", "three"])
        assert_frame_equal(df, df2)
        ds.df = None
        self.assertErr("TypeError", ds.wunique_, "col")

    def test_daterange(self):
        dates = dates = pd.date_range('20130101', periods=6)
        df1 = pd.DataFrame(dates, columns=["one"])
        ds.df = df1
        ds.daterange("one", "2013-01-02", "+", days=2)
        dates2 = pd.date_range('20130102', periods=3)
        df2 = pd.DataFrame(dates2, columns=["one"], index=[1, 2, 3])
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds2 = ds.daterange_("one", "2013-01-02", "+", days=2)
        assert_frame_equal(ds2.df, df2)
        ds.df = df1
        ds.daterange("one", "2013-01-06", "-", days=2)
        dates3 = pd.date_range('20130104', periods=3)
        df3 = pd.DataFrame(dates3, columns=["one"], index=[3, 4, 5])
        assert_frame_equal(ds.df, df3)
        ds.df = None
        ds.daterange_("one", "2013-01-02", "+", days=2)
        self.assertRaises(AttributeError)
        ds.daterange("one", "2013-01-02", "+", days=2)
        self.assertRaises(AttributeError)

    def test_subset(self):
        df1 = pd.DataFrame([["one", "one"], ["two", "two"],
                            ["three", "three"]])
        ds.df = df1
        ds.subset(2)
        df2 = pd.DataFrame([["one", "one"], ["two", "two"]])
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds2 = ds.subset_(0, 2)
        assert_frame_equal(ds2.df, df2)
        ds.df = None
        ds.subset(2)
        self.assertRaises(AttributeError)
        ds.subset_(2)
        self.assertRaises(AttributeError)

    """def test_nowrange(self):
        vdates = list(pd.date_range(datetime.datetime.now(), periods=6))
        dates = []
        for d in vdates:
            dates.append([d])
        df1 = pd.DataFrame(dates, columns=["one"])
        ds.df = df1
        ds.nowrange("one", 3)
        dates2 = dates[:3]
        df2 = pd.DataFrame(dates2, columns=["one"])
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds2 = ds.nowrange_("one", 3)
        assert_frame_equal(ds2.df, df2)
        ds.df = None
        ds.nowrange("one", 3)
        self.assertRaises(AttributeError)
        ds.nowrange_("one", 3)
        self.assertRaises(AttributeError)"""

    def test_limit(self):
        df1 = pd.DataFrame([["one", "three"], ["two", "four"]])
        ds.df = df1
        ds2 = ds.limit_(1)
        df2 = pd.DataFrame([["one", "three"]])
        assert_frame_equal(ds2.df, df2)
        ds.df = df1
        ds.limit(1)
        assert_frame_equal(ds.df, df2)
        ds.df = None
        ds.limit_()
        self.assertRaises(AttributeError)
        ds.limit()
        self.assertRaises(AttributeError)
