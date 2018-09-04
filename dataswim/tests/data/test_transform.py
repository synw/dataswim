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
        ds.dateindex("date")
        ds.df = ds._resample_(time_period="1M", method="mean", num_col="num",
                             fill_col=None, dateindex=None, index_col=None)
        ds.df = df1
        ds.dateindex("date")
        self.assertErr(None, ds._resample_, time_period="1M",
                       method="sum", num_col=None, fill_col=None,
                       dateindex="wrong", index_col=None)
        self.assertErr(None, ds._resample_, time_period="1M",
                       method="wrong", num_col=None, fill_col=None,
                       dateindex="date", index_col=None)
        self.assertErr(None, ds._resample_, time_period="1M",
                       method="sum", num_col="n", fill_col="wrong",
                       dateindex="wrong", index_col=None)

    def test_sum(self):
        df1 = pd.DataFrame([1, 2])
        ds.df = df1
        self.assertEqual(ds.sum_(0), 3)
        ds.df = None
        self.assertErr("TypeError", ds.sum_, 0)

    def test_reverse(self):
        df1 = pd.DataFrame([1, 2], index=[1,2])
        ds.df = df1
        df2 = pd.DataFrame([2, 1], index=[2, 1])
        ds.reverse()
        assert_frame_equal(ds.df, df2)
        ds.df = None
        self.assertErr("AttributeError", ds.reverse)

    def test_sort(self):
        df1 = pd.DataFrame([2, 1])
        ds.df = df1
        df2 = pd.DataFrame([1, 2])
        ds.sort(0)
        self.assertEqual(list(ds.df), list(df2))
        ds.df = None
        self.assertErr("AttributeError", ds.sort, 0)

    def test_apply(self):
        df1 = pd.DataFrame([[1,2], [1,2]], columns = ["one", "two"])
        ds.df = df1

        def ap(row):
            return row + 1

        ds.apply(ap, "one")
        df2 = pd.DataFrame([[2,2], [2,2]], columns = ["one", "two"])
        assert_frame_equal(ds.df, df2)
        ds.df = pd.DataFrame([[1,2], [1,2]], columns = ["one", "two"])
        ds.apply(ap)
        df3 = pd.DataFrame([[2,3], [2,3]], columns = ["one", "two"])
        assert_frame_equal(ds.df, df3)
        ds.df = None
        self.assertErr("TypeError", ds.apply, ap, "one")

    def test_replace(self):
        df1 = pd.DataFrame([[1,2], [1, 2]], columns=["one", "two"])
        ds.df = df1
        df2 = pd.DataFrame([[2,2], [2, 2]], columns=["one", "two"])
        ds.replace("one", 1, 2)
        self.assertEqual(list(ds.df), list(df2))
        ds.df = None
        self.assertErr("TypeError", ds.replace, "one", 1, 2)

    def test_pivot(self):
        df1 = pd.DataFrame([["n2", 1], ["n1", 2], ["n1", 1]],
                     columns = ["name", "val"])
        ds.df = df1
        ds.pivot("name")
        df2 = pd.DataFrame([1.5, 1.0], columns = ["val"], index=["n1", "n2"])
        assert_frame_equal(ds.df, df2, check_names=False)
        ds.df = df1
        ds2 = ds.pivot_("name")
        assert_frame_equal(ds2.df, df2, check_names=False)
        ds.df = None
        self.assertErr(None, ds.pivot_, "name")
        self.assertErr(None, ds.pivot, "name")

    def test_concat(self):
        df1 = pd.DataFrame([1,2])
        df2 = pd.DataFrame([3,4])
        ds.df = df1
        ds2 = ds.new_(df2)
        ds.concat(ds, ds2)
        df3 = pd.DataFrame([1,2,3,4])
        self.assertEqual(list(ds.df), list(df3))
        ds.df = df1
        ds2 = ds.concat_(ds, ds2)
        self.assertEqual(list(ds2.df), list(df3))
        ds2 = None
        self.assertErr(None, ds.concat_, ds, ds2)
        self.assertErr(None, ds.concat, ds, ds2)

    def test_split(self):
        df1 = pd.DataFrame([[1], [2], [1], [2]], columns=["val"])
        ds.df = df1
        dsd = ds.split_("val")
        d = {1: "<DataSwim object | 2 rows>", 2: "<DataSwim object | 2 rows>"}
        self.assertDictEqual(str(dsd), d)


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
