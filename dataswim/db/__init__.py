from numpy.core.numeric import nan
import dataset
import pandas as pd
from goerr import err
from .infos import Info
from .select import Select
from .relations import Relation
from .insert import Insert


class Db(Info, Select, Insert, Relation):
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
            self.err(e, self.connect, "Can not connect to database")
            return
        if self.db is None:
            self.err("Database" + url + " not found", self.connect)
            return
        if self.autoprint is True:
            self.ok("Db", self.db.url, "connected")

    def load(self, table, dateindex=None, index_col=None, fill_col=None):
        """
        Set the main dataframe from a table's data
        """
        try:
            self.df = self._load(table, dateindex, index_col, fill_col)
        except Exception as e:
            self.err(e, self.load, "Can not load table " + table)

    def load_(self, table, dateindex=None, index_col=None, fill_col=None):
        """
        Returns a DataSwim instance from a table's data
        """
        try:
            df = self._load(table, dateindex, index_col, fill_col)
            return self.clone_(df)
        except Exception as e:
            self.err(e, self.load_, "Can not load table " + table)

    def _load(self, table, dateindex, index_col, fill_col):
        """
        Set the main dataframe or return table's data
        """
        self._check_db()
        try:
            df = self.getall(table)
        except Exception as e:
            self.err(e, self._load, "Can not fetch data from table " + table)
            return self.df
        try:
            ds2 = self.transform_(dateindex, index_col, fill_col, df=df)
        except Exception as e:
            self.err(e, self.load, "Can not transform dataframe")
            return self.df
        if self.autoprint is True:
            self.ok("Data loaded from table", table)
        return ds2.df

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

    def _check_db(self):
        """
        Checks the database connection
        """
        if self.db is None:
            self.err(self._check_db, "Database not connected")
