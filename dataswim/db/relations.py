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
        return self.clone(df)

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
            print("START")
            try:
                # df.loc[df[id_field] == ]['A'].values

                print("ROW", row, "\nFIELD", origin_field)
                orow = row[origin_field]
                print('OROW', orow)
                serie = df.loc[orow]
            except:
                self.warning("Can not find serie")
                return nan
            print("SERIE", serie)
            try:
                val = serie[origin_field]
            except:
                self.warning("Can not find value in serie")
                return nan
            print("VAL", val)
            try:
                endval = search_ds.exact_(id_field, val).first_()[search_field]
                print("ENDVAL", endval)
                return endval
            except:
                print("NAN EXACT", val)
                return nan
        try:
            df = df.reset_index(drop=True)
            df = df.set_index(id_field)
        except Exception as e:
            self.err(e, self._relation, "Can not set index for relation")
            return
        try:
            df = df.copy()
            df[destination_field] = df.apply(set_rel, axis=1)
        except Exception as e:
            self.err(e, self._relation, "Can not get relation data")
            return
        return df
