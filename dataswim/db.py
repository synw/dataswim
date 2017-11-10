# -*- coding: utf-8 -*-

from __future__ import print_function
import dataset
import pandas as pd
from goerr import err
from numpy.core.numeric import nan


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
        try:
            self.db = dataset.connect(url)
        except Exception as e:
            err.new(e)
        if self.db is None:
            err.new("Database" + url + " not found", self.connect)
            err.trace()
        if self.autoprint is True:
            self.ok("Db", self.db.url, "connected")

    def load(self, table):
        """
        Set the main dataframe from a table's data
        """
        self._check_db()
        self._load(table, True)

    def load_(self, table):
        """
        Returns a DataSwim instance from a table's data
        """
        self._check_db()
        return self.new(self._load(table, False))

    def _load(self, table, main=True):
        """
        Set the main dataframe or return table's data
        """
        df = self.getall(table)
        if df is None:
            print("Can not get table " + table + " values")
        if main is True:
            self.df = df
        else:
            return df

    def load_django_(self, query):
        """
        Returns a DataSwim instance from a django orm query
        """
        self._check_db()
        return self.new(pd.DataFrame(list(query.values())))

    def load_django(self, query):
        """
        Set a main dataframe from a django orm query
        """
        self._check_db()
        self.df = pd.DataFrame(list(query.values()))

    def tables(self, name=None, p=True):
        """
        Print existing tables in a database
        """
        self._check_db()
        t = self.db.tables
        if name is not None:
            pmodels = [x for x in t if name in x]
        else:
            pmodels = t
        if p is True:
            print(pmodels)
        return pmodels

    def table(self, t=None, p=True):
        """
        Display info about a table
        """
        self._check_db()
        if t is None:
            df = self.df
        else:
            df = self.getall(t)
        if p is True:
            num = len(self.df.index)
            print(num, "rows")
            print("Fields:", ", ".join(list(df)))
        return df.head()

    def count_rows(self, name, p=True):
        """
        Count rows for a table
        """
        self._check_db()
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
        self._check_db()
        if table not in self.db.tables:
            err.new("The table " + table + " does not exists", self.getall)
            err.trace()
            return
        res = self.db[table].all()
        df = pd.DataFrame(list(res))
        return df

    def relation_(self, search_ds, origin_field, search_field, destination_field=None, id_field="id"):
        """
        Returns a DataSwim instance with a column filled from a relation foreign key 
        """
        self._check_db()
        return self._relation(search_ds, origin_field, search_field, destination_field, id_field, False)

    def relation(self, search_ds, origin_field, search_field, destination_field=None, id_field="id"):
        """
        Add a column to the main dataframe from a relation foreign key 
        """
        self._check_db()
        return self._relation(search_ds, origin_field, search_field, destination_field, id_field, True)

    def _relation(self, search_ds, origin_field, search_field, destination_field=None, id_field="id", main=True):
        """
        Add a column to the main dataframe from a relation foreign key 
        """
        df = self.df.copy()

        if destination_field is None:
            destination_field = search_field
        df[destination_field] = None

        def set_rel(row):
            # print(row)
            # return
            serie = df.loc[row[origin_field]]
            val = serie[origin_field]
            print(val, id_field)
            try:
                #print("Search", str(type(val)))
                d = search_ds.exact(val, search_field)
            except Exception as e:
                return nan
                #self.err(e, "can not find exact key", self._relation)
                # return
            try:
                val = d.first(False)[search_field]
                return val
            except Exception as e:
                return nan
        try:
            df = df.reset_index(drop=True)
            #df = df.set_index(id_field)
            df[destination_field] = df.apply(set_rel, axis=1)
        except Exception as e:
            self.err(e)
            return
        if main is True:
            self.df = df
        else:
            return self.new(df)

    def insert(self, table, records, create_cols=True):
        """
        Insert one or many records in the database from a dictionary or a list of dictionaries
        """
        self._check_db()
        table = self.db[table]
        t = type(records)
        if t == dict:
            func = table.insert
        elif t == list:
            func = table.insert_many
        else:
            err.new("Rows datatype " + str(t) +
                    " not valid: use a list or a dictionary")
            err.throw()
        if create_cols is True:
            func(records, ensure=True)
        else:
            func(records)
        if self.autoprint is True:
            self.ok("Rows inserted in the database")

    def to_db(self, table, db_url=None):
        """
        Save the main dataframe to the database
        """
        if self.db is None and db_url is None:
            err.new(
                "Please connect a database before or provide a database url", self.to_db)
            err.throw()
        if db_url is not None:
            self.connect(db_url)
        dic = self.to_records_()
        self.insert(table, dic)

    def _check_db(self, friendly=False):
        """
        Checks the database connection
        """
        if self.db is None:
            err.new("Please connect a database before or provide a database url")
            if friendly is False:
                err.throw()
            else:
                err.trace()
