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

    def relation(self, search_ds, origin_field, search_field, destination_field=None, id_field="id"):
        """
        Add a column to the main dataframe from a relation foreign key 
        """
        df = self._relation(search_ds, origin_field,
                            search_field, destination_field, id_field)
        self.df = df

    def relation_(self, search_ds, origin_field, search_field, destination_field=None, id_field="id"):
        """
        Returns a DataSwim instance with a column filled from a relation foreign key 
        """
        df = self._relation(search_ds, origin_field,
                            search_field, destination_field, id_field)
        return self.clone_(df)

    def _relation(self, search_ds, origin_field, search_field, destination_field, id_field):
        """
        Add a column to the main dataframe from a relation foreign key 
        """
        try:
            self._check_db()
        except Exception as e:
            self.err(e, self.count_rows, "Can not connect to database")
            return
        df = self.df.copy()
        if destination_field is None:
            destination_field = search_field
        df[destination_field] = None

        def set_rel(row):
            try:
                origin_val = row[origin_field]
                end_val = search_ds.df.loc[search_ds.df[id_field]
                                           == origin_val][search_field].values[0]
                return end_val
            except:
                return nan
        """
        try:
            df = df.reset_index(drop=True)
            df = df.set_index(origin_field)
        except Exception as e:
            self.err(e, self._relation, "Can not set index for relation")
            return
        """
        try:
            df = df.copy()
            df[destination_field] = df.apply(set_rel, axis=1)
        except Exception as e:
            self.err(e, self._relation, "Can not get relation data")
            return
        return df
