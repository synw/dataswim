

class Insert():
    """
    A class to handle data ingestion by the database
    """

    def insert(self, table, records, create_cols=True):
        """
        Insert one or many records in the database from a dictionary or a list of dictionaries
        """
        self._check_db()
        table = self.db[table]
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
            func(records, ensure=True)
        else:
            func(records)
        if self.autoprint is True:
            self.ok("Rows inserted in the database")

    def to_db(self, table, db_url=None):
        """
        Save the main dataframe to the database
        """
        if self.db is None and db_url is None:
            msg = "Please connect a database before or provide a database url"
            self.err(self.to_db, msg)
        if db_url is not None:
            self.connect(db_url)
        dic = self.to_records_()
        self.insert(table, dic)
