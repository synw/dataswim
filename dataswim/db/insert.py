from .base import DbBase
from typing import List
from sqlalchemy.types import SchemaType
from ..errors import Error
from ..messages import Message


class Insert(DbBase, Error, Message):
    """
    A class to handle data ingestion by the database
    """

    def __init__(self, db=None):
        """
        Initialize with an empty db
        """
        self.db = db

    def insert(self, table: str, records: dict, create_cols: bool=False,
               dtypes: List[SchemaType]=None):
        """Insert one or many records in the database from a dictionary
         or a list of dictionaries

        :param table: the table to insert into
        :type table: str
        :param records: a dictionnary or list of dictionnaries
         of the data to insert
        :type records: dict
        :param create_cols: create the columns if they don't exist, defaults
         to False
        :type create_cols: bool, optional
        :param dtypes: list of SqlAlchemy table types, defaults to None. The
         types are infered if not provided
        :type dtypes: SchemaType, optional
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
               dtypes: List[SchemaType]=None, pks: List[str]=["id"]):
        """Upsert a record in a table

        :param table: the table to upsert into
        :type table: str
        :param record: dictionary with the data to upsert
        :type record: dict
        :param create_cols: create the columns if it doesn't exist,
         defaults to False
        :type create_cols: bool, optional
        :param dtypes: list of SqlAlchemy column types, defaults to None
        :type dtypes: List[SchemaType], optional
        :param pks: if rows with matching pks exist they will be updated,
         otherwise a new row is inserted in the table, defaults to ["id"]
        :type pks: List[str], optional
        """
        if self._check_db() is False:
            return
        try:
            self.db[table].upsert(record, pks, create_cols, dtypes)
        except Exception as e:
            self.err(e, "Can not upsert data")
            return
        self.ok("Upserted record")

    def update_table(self, table: str, pks: List[str]=['id']):
        """Update records in a database table from the main dataframe

        :param table: table to update
        :type table: str
        :param pks: if rows with matching pks exist they will be updated,
         otherwise a new row is inserted in the table, defaults to ["id"]
        :type pks: List[str], optional
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

    def to_db(self, table: str, dtypes: List[SchemaType]=None):
        """Save the main dataframe to the database

        :param table: the table to create
        :type table: str
        :param dtypes: SqlAlchemy columns type, defaults to None,
         will be infered if not provided
        :type dtypes: List[SchemaType], optional
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
