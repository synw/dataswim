# -*- coding: utf-8 -*-

import dataset
import pandas as pd


class Db():
    """
    Class for manipulating databases
    """

    def __init__(self, db=None):
        """
        Initialize with an empty db
        """
        self.db = db

    def connect(self, url):
        """
        Connect to the database and set it as main database
        """
        self.db = dataset.connect(url)

    def load(self, table):
        """
        Set the main dataframe from a table's data
        """
        self.df = self.getall(table)

    def tables(self, name=None, p=True):
        """
        Print existing tables in a database
        """
        t = self.db.tables
        if name is not None:
            pmodels = [x for x in t if name in x]
        else:
            pmodels = t
        if p is True:
            print(pmodels)
        return pmodels

    def count_rows(self, name, p=True):
        """
        Count rows for a table
        """
        data = {}
        for m in self.tables(name, False):
            num = self.db[m].count()
            data[m] = num
            if p is True and num > 0:
                print(m, num)
        print("[end]")
        return data

    def getall(self, table):
        """
        Get all rows values for a table
        """
        res = self.db[table].all()
        df = pd.DataFrame(list(res))
        return df

    def table(self, t=None, p=True):
        """
        Display info about a table
        """
        if t is None:
            df = self.df
        else:
            df = self.getall(t)
        num = len(self.df.index)
        if p is True:
            print(num, "rows")
            print("Fields:", ", ".join(list(df)))
        return df.head()