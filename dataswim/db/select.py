import pandas as pd


class Select():
    """
    A class to retrieve data from the database
    """

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
            self._check_db()
            return self.new(self._load(table))
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

    def getall(self, table):
        """
        Get all rows values for a table
        """
        try:
            self._check_db()
        except Exception as e:
            self.err(e, self.getall, "Can not connect to database")
            return
        if table not in self.db.tables:
            self.warning("The table " + table +
                         " does not exists", self.getall)
            return
        try:
            res = self.db[table].all()
            df = pd.DataFrame(list(res))
            return df
        except Exception as e:
            self.err(e, self.getall, "Error retrieving data in table")
