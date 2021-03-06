from numpy.core.numeric import nan
from pandas import DataFrame
from .base import DbBase


class Relation(DbBase):
    """
    A class to handle database relations
    """

    def relation(self, table: str, origin_field: str, search_field: str,
                 destination_field: str=None, id_field: str="id"):
        """Add a column to the main dataframe from a relation foreign key

        :param table: the table to select from
        :type table: str
        :param origin_field: the column name in the origin table to
         search from, generally an id column
        :type origin_field: str
        :param search_field: the column name in the foreign table
        :type search_field: str
        :param destination_field: name of the column to be created with
         the data in the datframe, defaults to None, will be named as
         the origin_field if not provided
        :type destination_field: str, optional
        :param id_field: name of the primary key to use, defaults to "id"
        :type id_field: str, optional

        example: ``ds.relation("product", "category_id", "name")``
        """
        df = self._relation(table, origin_field,
                            search_field, destination_field, id_field)
        self.df = df

    def relation_(self, table: str, origin_field: str, search_field: str,
                  destination_field=None, id_field="id") -> DataFrame:
        """Returns a DataSwim instance with a column filled from a relation
         foreign key

        :param table: the table to select from
        :type table: str
        :param origin_field: the column name in the origin table to
         search from, generally an id column
        :type origin_field: str
        :param search_field: the column name in the foreign table
        :type search_field: str
        :param destination_field: name of the column to be created with
         the data in the datframe, defaults to None, will be named as
         the origin_field if not provided
        :type destination_field: str, optional
        :param id_field: name of the primary key to use, defaults to "id"
        :type id_field: str, optional
        :return: a pandas DataFrame
        :rtype: DataFrame
        """
        df = self._relation(table, origin_field,
                            search_field, destination_field, id_field)
        return self._duplicate_(df)

    def _relation(self, table, origin_field, search_field, destination_field,
                  id_field):
        """
        Add a column to the main dataframe from a relation foreign key 
        """
        self.start("Processing relation",
                   origin_field, "->", search_field)
        search_ds = self._duplicate_(db=self.db, quiet=True)
        search_ds.load(table)
        df = self.df.copy()
        if destination_field is None:
            destination_field = search_field
        df[destination_field] = None

        if origin_field not in self.df.columns.values:
            msg = "Can not find field " + origin_field + " in dataset: "
            msg += "found fields " + ", ".join(list(self.df.columns.values))
            self.warning(msg)
            return
        if search_field not in search_ds.df.columns.values:
            msg = "Can not find field " + search_field + \
                " in related dataset: "
            msg += "found fields " + \
                ", ".join(list(search_ds.df.columns.values))
            self.warning(msg)
            return

        def set_rel(row):
            try:
                origin_val = row[origin_field]
                end_val = search_ds.df.loc[
                    search_ds.df[id_field] ==
                    origin_val][search_field].values[0]
                return end_val
            except Exception:
                return nan

        try:
            df = df.copy()
            df[destination_field] = df.apply(set_rel, axis=1)
        except Exception as e:
            self.err(e, self._relation, "Can not get relation data")
            return
        self.end("Finished processing relation")
        return df
