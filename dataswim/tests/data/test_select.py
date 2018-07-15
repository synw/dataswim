# -*- coding: utf-8 -*-
import datetime
import pandas as pd
import numpy as np
from pandas.testing import assert_series_equal, assert_frame_equal
from dataswim.tests.base import BaseDsTest
from dataswim import ds

ds.errs_traceback = False


class TestDsDataSelect(BaseDsTest):

    def test_first(self):
        df1 = pd.DataFrame([["one", "three"], ["two", "four"]])
        ds.df = df1
        first = ds.first_()
        res = pd.Series(["one", "three"], name=0)
        assert_series_equal(first, res)
        ds.df = None
        _ = ds.first_()
        self.assertRaises(AttributeError)

    def test_unique(self):
        df1 = pd.DataFrame([["one", "one", "three"], ["two", "two", "four"]])
        ds.df = df1
        data = ds.unique_(0)
        res = ["one", "two"]
        self.assertEqual(data, res)
        ds.df = None
        _ = ds.unique_(0)
        self.assertRaises(AttributeError)

    def test_range(self):
        dates = pd.date_range('20130101', periods=6)
        vals = np.random.randn(6)
        df1 = pd.DataFrame(vals, index=dates)
        ds.df = df1
        ds.vrange(days=2)
        dates2 = pd.date_range('20130101', periods=3)
        df2 = pd.DataFrame(vals[:3], index=dates2)
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds2 = ds.range_(days=2)
        assert_frame_equal(ds2.df, df2)
        ds.df = None
        ds.vrange(days=2)
        self.assertRaises(AttributeError)
        _ = ds.range_(days=2)
        self.assertRaises(AttributeError)

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
        _ = ds.daterange_("one", "2013-01-02", "+", days=2)
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
        _ = ds.subset_(2)
        self.assertRaises(AttributeError)

    def test_nowrange(self):
        vdates = list(pd.date_range(datetime.datetime.now(), periods=6))
        dates = []
        for d in vdates:
            dates.append([d])
        vals = np.random.randn(6)
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
        _ = ds.nowrange_("one", 3)
        self.assertRaises(AttributeError)

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
        _ = ds.limit_()
        self.assertRaises(AttributeError)
        ds.limit()
        self.assertRaises(AttributeError)
