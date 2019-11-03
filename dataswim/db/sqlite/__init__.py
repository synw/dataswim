import sqlite3
from sqlite3 import Error as SqlErr
from ...base import DsBase


class SqliteDb(DsBase):

    _conn = None
    _cursor = None
    _buffer = None

    def sconnect(self, url: str):
        try:
            self._conn = sqlite3.connect(url)
            self._cursor = self._conn.cursor()
        except SqlErr as e:
            self.err(e, "Can not connect Sqlite database at "+url)
            return
        self.ok("Database connected")

    def scommit(self):
        self._conn.commit()

    def sq_(self, query: str):
        try:
            return self._cursor.execute(query)
        except Exception as e:
            self.err(e, "Can not query Sqlite database")

    def sqm_(self, query: str, values):
        try:
            return self._cursor.executemany(query, values)
        except Exception as e:
            self.err(e, "Can not query Sqlite database")
