import dataset
from .base import DbBase
from ..errors import Error


class Query(DbBase, Error):

    def query(self, q: str) -> dataset.util.ResultIter:
        """Query the database

        :param q: the query to perform
        :type q: str
        :return: a dictionary with the query results
        :rtype: dataset.util.ResultIter
        """
        try:
            self._check_db()
        except Exception as e:
            self.err(e, "Can not connect to database")
            return
        try:
            result = self.db.query(q)
            return result
        except Exception as e:
            self.err(e, "Can not query the database")
