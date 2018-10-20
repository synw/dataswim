from numpy.core.numeric import nan


class Relation():
    """
    A class to handle database relations
    """

    def __init__(self, db=None):
        """
        Initialize with an empty db
        """
        self.db = db

    def relation(self, table, origin_field, search_field, destination_field=None,
                 id_field="id"):
        """
        Add a column to the main dataframe from a relation foreign key 
        """
        df = self._relation(table, origin_field,
                            search_field, destination_field, id_field)
        self.df = df

    def relation_(self, table, origin_field, search_field, destination_field=None,
                  id_field="id"):
        """
        Returns a DataSwim instance with a column filled from a relation foreign key 
        """
        df = self._relation(table, origin_field,
                            search_field, destination_field, id_field)
        return self._duplicate_(df)

    def _relation(self, table, origin_field, search_field, destination_field, id_field):
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
            msg = "Can not find field " + search_field + " in related dataset: "
            msg += "found fields " + \
                ", ".join(list(search_ds.df.columns.values))
            self.warning(msg)
            return

        def set_rel(row):
            try:
                origin_val = row[origin_field]
                end_val = search_ds.df.loc[search_ds.df[id_field]
                                           == origin_val][search_field].values[0]
                return end_val
            except:
                return nan

        try:
            df = df.copy()
            df[destination_field] = df.apply(set_rel, axis=1)
        except Exception as e:
            self.err(e, self._relation, "Can not get relation data")
            return
        self.end("Finished processing relation")
        return df
