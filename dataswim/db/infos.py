from goerr.colors import colors


class Info():
    """
    A class to handle information requests from the database
    """

    def __init__(self, db=None):
        """
        Initialize with an empty db
        """
        self.db = db

    def tables(self, name=None):
        """
        Print existing tables in a database
        """
        pmodels = self._tables(name)
        if pmodels is None:
            return
        num = len(pmodels)
        s = "s"
        if num == 1:
            s = ""
        msg = "Found " + colors.bold(str(num)) + " table" + s + ":\n"
        msg += "\n".join(pmodels)
        self.info(msg)

    def tables_(self, name=None):
        """
        Print existing tables in a database
        """
        try:
            pmodels = self._tables(name)
        except Exception as e:
            self.err(e, "Can not print tables")
        return pmodels

    def _tables(self, name):
        """
        Print existing tables in a database
        """
        self._check_db()
        t = self.db.tables
        if name is not None:
            pmodels = [x for x in t if name in x]
        else:
            pmodels = t
        if pmodels is None:
            msg = "No tables found in the database"
            if name is not None:
                msg = "No tables found in the database for table like " + name
            self.warning(msg)
            return
        return pmodels

    def table(self, t=None, quiet=False):
        """
        Display info about a table
        """
        try:
            self._check_db()
        except Exception as e:
            self.err(e, self.table, "Can not connect to database")
            return
        if t is None:
            df = self.df
        else:
            try:
                df = self.getall(t)
            except Exception as e:
                self.err(e, self.table, "Can not get records from database")
        if self.df is None:
            self.warning("Table", t, "does not contain any record")
            return
        if self.autoprint is True and quiet is False:
            num = len(self.df)
            print(num, "rows")
            print("Fields:", ", ".join(list(df)))

    def count_rows(self, name, zero=False):
        """
        Count rows for a table
        """
        try:
            self._check_db()
        except Exception as e:
            self.err(e, self.count_rows, "Can not connect to database")
            return
        total = 0
        self.start("Counting rows in tables like", colors.bold(name))
        for t in self.tables_(name):
            num = self.db[t].count()
            total += num
            if self.autoprint is True:
                if num > 0 or zero is True:
                    msg = t + ":" + colors.bold(num)
                    print(msg)
        self.end("Found a total of", colors.bold(total), "rows")
