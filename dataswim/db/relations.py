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

    def relation_(self, search_ds, origin_field, search_field, destination_field=None, id_field="id"):
        """
        Returns a DataSwim instance with a column filled from a relation foreign key 
        """
        self._check_db()
        return self._relation(search_ds, origin_field, search_field, destination_field, id_field, False)

    def relation(self, search_ds, origin_field, search_field, destination_field=None, id_field="id"):
        """
        Add a column to the main dataframe from a relation foreign key 
        """
        self._check_db()
        return self._relation(search_ds, origin_field, search_field, destination_field, id_field, True)

    def _relation(self, search_ds, origin_field, search_field, destination_field=None, id_field="id", main=True):
        """
        Add a column to the main dataframe from a relation foreign key 
        """
        df = self.df.copy()

        if destination_field is None:
            destination_field = search_field
        df[destination_field] = None

        def set_rel(row):
            serie = df.loc[row[origin_field]]
            val = serie[origin_field]
            print(val, id_field)
            try:
                #print("Search", str(type(val)))
                d = search_ds.exact_(val, search_field)
            except:
                return nan
            try:
                val = d.first(False)[search_field]
                return val
            except:
                return nan
        try:
            df = df.reset_index(drop=True)
            df = df.set_index(id_field)
            df[destination_field] = df.apply(set_rel, axis=1)
        except Exception as e:
            self.err(e, self._relation, "Can not set index for relation")
            return
        if main is True:
            self.df = df
        else:
            return self.new(df)
