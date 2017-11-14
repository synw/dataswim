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
        try:
            self.df = self._load(table)
        except Exception as e:
            self.err(e)

    def load_(self, table):
        """
        Returns a DataSwim instance from a table's data
        """
        try:
            return self.clone_(self._load(table))
        except Exception as e:
            self.err(e)

    def _load(self, table):
        """
        Set the main dataframe or return table's data
        """
        try:
            self._check_db()
        except Exception as e:
            self.err(e, self.count_rows, "Can not connect to database")
            return
        try:
            df = self.getall(table)
        except Exception as e:
            self.err(e, self.count_rows, "Can load data from table " + table)
            return
        if self.autoprint is True:
            self.ok("Data loaded from table", table)
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

    def _check_db(self, friendly=False):
        """
        Checks the database connection
        """
        if self.db is None:
            self.err(
                self._check_db, "Database not connected")
