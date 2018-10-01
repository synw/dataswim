import pandas as pd


class Select():
    """
    A class to retrieve data from the database
    """

    def __init__(self, db=None):
        """
        Initialize with an empty db
        """
        self.db = db

    def getall(self, table):
        """
        Get all rows values for a table
        """
        try:
            self._check_db()
        except Exception as e:
            self.err(e, "Can not connect to database")
            return
        if table not in self.db.tables:
            self.warning("The table " + table + " does not exists")
            return
        try:
            res = self.db[table].all()
            df = pd.DataFrame(list(res))
            return df
        except Exception as e:
            self.err(e, "Error retrieving data in table")
