# -*- coding: utf-8 -*-
import pandas as pd
from pandas.testing import assert_series_equal
from sklearn import linear_model
from dataswim.tests.base import BaseDsTest
from dataswim import ds

ds.errs_traceback = False


class TestDsDataStats(BaseDsTest):

    def test_lreg(self):
        df1 = pd.DataFrame([["2001/01/01", 1], ["2001/01/02", 2],
                            ["2001/01/03", 3], ["2001/01/04", 3]],
                            columns = ["date", "value"])
        ds.df = df1
        ds.timestamps("date")
        ds.lreg("Timestamps", "value")
        expected = pd.Series([1.2, 1.9, 2.6, 3.3], name="regression")
        assert_series_equal(ds.df["regression"], expected)
        ds.df = None
        self.assert_err("TypeError", ds.lreg, "x", "y")
