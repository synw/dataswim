

class Insert():
    """
    A class to handle data ingestion by the database
    """

    def __init__(self, db=None):
        """
        Initialize with an empty db
        """
        self.db = db

    def insert(self, table, records, create_cols=True):
        """
        Insert one or many records in the database from a dictionary or a list of dictionaries
        """
        self._check_db()
        try:
            table = self.db[table]
        except Exception as e:
            self.err(e, self.update_db, "Can not find table " + table)
        t = type(records)
        if t == dict:
            func = table.insert
        elif t == list:
            func = table.insert_many
        else:
            msg = "Rows datatype " + \
                str(t) + " not valid: use a list or a dictionary"
            self.err(self.insert, msg)
        if create_cols is True:
            try:
                func(records, ensure=True)
            except Exception as e:
                self.err(e, self.insert,
                         "Can not insert create columns and insert data")
            return
        else:
            try:
                func(records)
            except Exception as e:
                self.err(e, self.insert,
                         "Can not insert create columns and insert data")
            return
        if self.autoprint is True:
            self.ok("Rows inserted in the database")

    def update_db(self, table, keys=['id'], db_url=None):
        """
        Update records in a database table from the main dataframe
        """
        try:
            table = self.db[table]
        except Exception as e:
            self.err(e, self.update_db, "Can not find table " + table)
        if self.db is None and db_url is None:
            msg = "Please connect a database before or provide a database url"
            self.err(self.to_db, msg)
            return
        recs = self.to_records_()
        for rec in recs:
            table.insert_ignore(rec, keys, ensure=True)
        if self.autoprint is True:
            self.ok("Data updated in table", table)

    def to_db(self, table, db_url=None):
        """
        Save the main dataframe to the database
        """
        if self.db is None and db_url is None:
            msg = "Please connect a database before or provide a database url"
            self.err(self.to_db, msg)
            return
        if db_url is not None:
            self.connect(db_url)
        recs = self.to_records_()
        self.insert(table, recs)
        if self.autoprint is True:
            self.ok("Data inserted in table", table)
