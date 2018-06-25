import unittest
import pandas as pd


class BaseDsTest(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({"one": 1, "two": 2}, ["1", "2"])
