import pandas as pd
from pandas.testing import assert_frame_equal
from dataswim.tests.base import BaseDsTest
from dataswim import ds


class TestDsDataInit(BaseDsTest):

    def test_clone(self):
        ds.df = self.df
        ds2 = ds.clone_()
        assert_frame_equal(ds2.df, ds.df)
        ds2 = ds.clone_(df=self.df, db="db")
        ds2 = ds.new_()
        # error
        ds.df = None
        ds2 = ds.clone_()
        self.assertRaises(AttributeError)
        ds2 = ds.duplicate_(df="wrong")
        self.assertRaises(AttributeError)

    def test_set(self):
        ds.set(self.df)
        assert_frame_equal(self.df, ds.df)
        # errors
        ds.set("wrong")
        self.assertRaises(AttributeError)

    def test_backup_restore(self):
        ds.df = self.df
        ds.backup()
        ds.df = pd.DataFrame({"1": 1}, ["1"])
        ds.restore()
        assert_frame_equal(ds.df, self.df)
        # errors
        ds.df = "wrong"
        ds.backup()
        self.assertRaises(AttributeError)
        ds.df = self.df
        ds.backup_df = "wrong"
        ds.restore()
        self.assertRaises(AttributeError)
