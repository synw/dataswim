# -*- coding: utf-8 -*-
import pandas as pd
from pandas.testing import assert_frame_equal
from dataswim.tests.base import BaseDsTest
from dataswim import ds

ds.errs_traceback = False


class TestDsDataSearch(BaseDsTest):

    def test_contains(self):
        df1 = pd.DataFrame([["one x", "three"], ["two", "four"]])
        ds.df = df1
        ds.contains(0, "one")
        df2 = pd.DataFrame([["one x", "three"]])
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds2 = ds.contains_(0, "one")
        assert_frame_equal(ds2.df, df2)
        ds.df = None
        res = ds.contains_(0, "one")
        self.assertRaises(TypeError)
        ds.contains(0, "one")
        self.assertRaises(TypeError)

    def test_exact(self):
        df1 = pd.DataFrame([["one", "three"], ["two", "four"]])
        ds.df = df1
        ds.exact(0, "one")
        df2 = pd.DataFrame([["one", "three"]])
        assert_frame_equal(ds.df, df2)
        ds.df = df1
        ds2 = ds.exact_(0, "one")
        assert_frame_equal(ds2.df, df2)
        ds.df = None
        res = ds.exact_(0, "one")
        self.assertRaises(TypeError)
        ds.exact(0, "one")
        self.assertRaises(TypeError)

