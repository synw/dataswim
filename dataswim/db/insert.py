from .base import DbBase


class Insert(DbBase):
    """
    A class to handle data ingestion by the database
    """

    def __init__(self, db=None):
        """
        Initialize with an empty db
        """
        self.db = db

    def insert(self, table, records, create_cols=False, dtypes=None):
        """
        Insert one or many records in the database from a dictionary or a list of dictionaries
        """
        if self._check_db() is False:
            return
        try:
            table = self.db[table]
        except Exception as e:
            self.err(e, "Can not find table " + table)
        t = type(records)
        if t == dict:
            func = table.insert
        elif t == list:
            func = table.insert_many
        else:
            msg = "Rows datatype " + \
                str(t) + " not valid: use a list or a dictionary"
            self.err(msg)
        if create_cols is True:
            try:
                func(records, ensure=True, types=dtypes)
            except Exception as e:
                self.err(e, "Can not insert create columns and insert data")
            return
        else:
            try:
                func(records, types=dtypes)
            except Exception as e:
                self.err(e, "Can not insert data")
            return
        self.ok("Rows inserted in the database")

    def upsert(self, table: str, record: dict, create_cols: bool=False,
               dtypes: list=None, pks=["id"], namefields=["id"]):
        """
        Upsert a record in a table
        """
        try:
            self.db[table].upsert(record, pks, create_cols, dtypes)
        except Exception as e:
            self.err(e, "Can not upsert data")
            return
        names = ""
        for el in namefields:
            names += " " + record[el]
        self.ok("Upserted record"+names)

    def update_table(self, table, pks=['id']):
        """
        Update records in a database table from the main dataframe
        """
        if self._check_db() is False:
            return
        try:
            table = self.db[table]
        except Exception as e:
            self.err(e, "Can not find table " + table)
        if self.db is None:
            msg = "Please connect a database before or provide a database url"
            self.err(msg)
            return
        recs = self.to_records_()
        for rec in recs:
            table.insert_ignore(rec, pks, ensure=True)
        self.ok("Data updated in table", table)

    def to_db(self, table, dtypes=None):
        """
        Save the main dataframe to the database
        """
        if self._check_db() is False:
            return
        if table not in self.db.tables:
            self.db.create_table(table)
            self.info("Created table ", table)
        self.start("Saving data to database table " + table + " ...")
        recs = self.to_records_()
        self.insert(table, recs, dtypes)
        self.end("Data inserted in table", table)
