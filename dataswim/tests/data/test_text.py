# -*- coding: utf-8 -*-
import pandas as pd
from pandas.testing import assert_frame_equal
from dataswim.tests.base import BaseDsTest
from dataswim import ds

ds.errs_traceback = False


class TestDsDataText(BaseDsTest):

    def test_flat(self):
        df1 = pd.DataFrame([["one", "one"], ["two", "two"]],
                           columns=["one", "two"])
        ds.df = df1
        data = ds.flat_("one")
        self.assertEqual(data, '0 one 1 two')
        data = ds.flat_("one", False)
        self.assertEqual(data, 'one two')
        ds.df = None
        data = ds.flat_("one")
        self.assertRaises(TypeError)

    def test_mfw(self):
        df1 = pd.DataFrame([["one", "one"], ["two", "two"], ["one", "three"]],
                           columns=["one", "two"])
        ds.df = df1
        ds2 = ds.mfw_("one")
        df2 = pd.DataFrame([[2, "one"], [1, "two"]],
                           columns=["Frequency", "Word"]).set_index('Word')
        assert_frame_equal(ds2.df, df2)
        ds.df = None
        _ = ds.mfw_("one")
        self.assertRaises(TypeError)
