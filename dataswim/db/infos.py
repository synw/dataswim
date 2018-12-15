from goerr.colors import colors
from .base import DbBase


class Info(DbBase):
    """
    A class to handle information requests from the database
    """

    def tables(self):
        """Print the existing tables in a database

        :example: ``ds.tables()``
        """
        if self._check_db() == False:
            return
        try:
            pmodels = self._tables()
            if pmodels is None:
                return
            num = len(pmodels)
            s = "s"
            if num == 1:
                s = ""
            msg = "Found " + colors.bold(str(num)) + " table" + s + ":\n"
            msg += "\n".join(pmodels)
            self.info(msg)
        except Exception as e:
            self.err(e, "Can not print tables")

    def tables_(self) -> list:
        """Return a list of the existing tables in a database

        :return: list of the table names
        :rtype: list

        :example: ``tables = ds.tables_()``
        """
        if self._check_db() == False:
            return
        try:
            return self._tables()
        except Exception as e:
            self.err(e, "Can not print tables")

    def _tables(self):
        if self._check_db() == False:
            return
        pmodels = self.db.tables
        if pmodels is None:
            msg = "No tables found in the database"
            self.warning(msg)
            return
        return pmodels

    def table(self, name: str):
        """
        Display info about a table: number of rows
        and columns

        :param name: name of the table
        :type name: str

        :example: ``tables = ds.table("mytable")``
        """
        if self._check_db() == False:
            return
        try:
            res = self.getall(name)
        except Exception as e:
            self.err(e, self.table, "Can not get records from database")
            return
        if res is None:
            self.warning("Table", name, "does not contain any record")
            return
        num = len(res)
        self.info(num, "rows")
        self.info("Fields:", ", ".join(list(res)))
