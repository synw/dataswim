

class Info():
    """
    A class to handle information requests from the database
    """

    def __init__(self, db=None):
        """
        Initialize with an empty db
        """
        self.db = db

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
        return df.head()

    def count_rows(self, name, zero=False):
        """
        Count rows for a table
        """
        try:
            self._check_db()
        except Exception as e:
            self.err(e, self.count_rows, "Can not connect to database")
            return
        data = {}
        for m in self.tables(name, False):
            num = self.db[m].count()
            data[m] = num
            if self.autoprint is True:
                if num > 0 or zero is True:
                    print(m, num)
        print("[end]")
        return data
