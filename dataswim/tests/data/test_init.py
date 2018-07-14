import pandas as pd
from pandas.testing import assert_frame_equal
from dataswim.tests.base import BaseDsTest
from dataswim import ds

ds.errs_traceback = False


class TestDsDataInit(BaseDsTest):

    def test_clone_duplicate_(self):
        ds.df = self.df
        ds2 = ds.clone_()
        assert_frame_equal(ds2.df, ds.df)
        ds2 = ds.new_()
        # error clone
        ds.df = None
        ds2 = ds.clone_()
        self.assertRaises(AttributeError)
        ds.df = "wrong"
        ds2 = ds.clone_()
        self.assertRaises(AttributeError)
        ds2 = ds._duplicate_(self.df, "db", False)

    def test_load_json(self):
        data = self.df.to_json()
        ds.load_json(data)
        ds.load_json("wrong")
        self.assertRaises(ValueError)

    def test_load_csv(self):
        ds.load_csv(self.path+"/data/fixtures/data.csv")
        ds.datapath = self.path+"/data"
        ds.load_csv("data.csv")
        ds.load_csv(None)

    def test_load_excel(self):
        ds.load_excel(self.path+"/data/fixtures/data.xls")
        ds.load_excel("wrong")
        ds.load_excel(self.path+"/data/fixtures/empty.xls")

    def test_load_h5(self):
        ds.load_h5(self.path + "/data/fixtures/data.h5")
        ds.load_h5("wrong")

    def test_dateparser(self):
        dp = ds.dateparser()
        dp(["12/01/2012", "13/01/2012"])

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
        ds.backup_df = None
        ds.restore()
        self.assertRaises(AttributeError)
