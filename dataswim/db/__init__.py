# @PydevCodeAnalysisIgnore
from numpy.core.numeric import nan
import dataset
from stuf import stuf
import pandas as pd
from .infos import Info
from .relations import Relation
from .insert import Insert
from .influxdb import InfluxDb


class Db(Info, Insert, Relation, InfluxDb):
    """
    Class for manipulating databases
    """

    def __init__(self):
        """
        Initialize with an empty database
        """
        self.db = db

    def connect(self, url: str):
        """Connect to the database and set it as main database

        :param url: path to the database, uses the Sqlalchemy format
        :type url: str

        :example: ``ds.connect("sqlite:///mydb.slqite")``
        """
        try:
            self.db = dataset.connect(url, row_type=stuf)
        except Exception as e:
            self.err(e, "Can not connect to database")
            return
        if self.db is None:
            self.err("Database " + url + " not found")
            return
        self.ok("Db", self.db.url, "connected")

    def load(self, table: str):
        """Set the main dataframe from a table's data

        :param table: table name
        :type table: str

        :example: ``ds.load("mytable")``
        """
        try:
            self.start("Loading data from table " + table)
            self.df = self._load(table)
            self.end("Data loaded from table " + table)
        except Exception as e:
            self.err(e, "Can not load table " + table)

    def load_(self, table: str) -> "Ds":
        """Returns a DataSwim instance from a table's data

        :param table: table name
        :type table: str
        :return: a dataswim instance
        :rtype: Ds

        :example: ``ds2 = ds.load_("mytable")``
        """
        try:
            self.start("Loading data from table " + table)
            df = self._load(table)
            ds2 = self.clone_(df)
            return ds2
            self.end("Data loaded from table " + table)
        except Exception as e:
            self.err(e, "Can not load data from table " + table)

    def _load(self, table: str):
        self._check_db()
        try:
            df = self.getall(table)
            return df
        except Exception as e:
            self.err(e, "Can not fetch data from table " + table)

    def load_django(self, query: "django query"):
        """Load the main dataframe from a django orm query

        :param query: django query from a model
        :type query: django query

        :example: ``ds.load_django(Mymodel.objects.all())``
        """
        try:
            self.df = self._load_django(query)
        except Exception as e:
            self.err(e, "Can not load data from query")

    def load_django_(self, query: "django query") -> "Ds":
        """Returns a DataSwim instance from a django orm query

        :param query: django query from a model
        :type query: django query
        :return: a dataswim instance with data from a django query
        :rtype: Ds

        :example: ``ds2 = ds.load_django_(Mymodel.objects.all())``
        """
        try:
            df = self._load_django(query)
            return self.clone_(df)
        except Exception as e:
            self.err(e, "Can not load data from query")

    def _load_django(self, query: "django query"):
        try:
            df = pd.DataFrame(list(query.values()))
            return df
        except Exception as e:
            self.err(e)

    def dftable_(self, name: str) -> pd.DataFrame:
        """
        Get a dataframe with all rows values for a table

        :param name: name of the table
        :type name: str
        :return: a pandas dataframe
        :rtype: pd.DataFrame

        :example: ``df = ds.dftable_("mytable")``
        """
        if self._check_db() is False:
            return
        if name not in self.db.tables:
            self.warning("The table " + name + " does not exists")
            return
        try:
            res = self.db[name].all()
            df = pd.DataFrame(list(res))
            return df
        except Exception as e:
            self.err(e, "Error retrieving data in table")

    def _check_db(self) -> bool:
        if self.db is None:
            self.warning("Database not connected")
            return False
        return True
