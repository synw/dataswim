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

    def _check_db(self, friendly=False):
        """
        Checks the database connection
        """
        if self.db is None:
            self.err(
                self._check_db, "Database not connected")
