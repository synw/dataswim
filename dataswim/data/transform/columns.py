from ...errors import Error
from ...messages import Message


class Columns(Error, Message):
    """
    Class to transform the dataframe's columns
    """

    def rename(self, source_col: str, dest_col: str):
        """
        Renames a column in the main dataframe

        :param source_col: name of the column to rename
        :type source_col: str
        :param dest_col: new name of the column
        :type dest_col: str

        :example: ``ds.rename("Col 1", "New col")``
        """
        try:
            self.df = self.df.rename(columns={source_col: dest_col})
        except Exception as e:
            self.err(e, self.rename, "Can not rename column")
            return
        self.ok("Column", source_col, "renamed")

    def add(self, col: str, value):
        """
        Add a column with default values

        :param col: column name
        :type col: str
        :param value: column value
        :type value: any

        :example: ``ds.add("Col 4", 0)``
        """
        try:
            self.df[col] = value
        except Exception as e:
            self.err(e, self.add, "Can not add column")

    def keep_(self, *cols) -> "Ds":
        """
        Returns a dataswim instance with a dataframe limited
        to some columns

        :param cols: names of the columns
        :type cols: str
        :return: a dataswim instance
        :rtype: Ds

        :example: ``ds2 = ds.keep_("Col 1", "Col 2")``
        """
        try:
            ds2 = self._duplicate_(self.df[list(cols)])
        except Exception as e:
            self.err(e, "Can not remove colums")
            return
        self.ok("Columns", " ,".join(cols), "kept")
        return ds2

    def keep(self, *cols):
        """
        Limit the dataframe to some columns

        :param cols: names of the columns
        :type cols: str

        :example: ``ds.keep("Col 1", "Col 2")``
        """
        try:
            self.df = self.df[list(cols)]
        except Exception as e:
            self.err(e, "Can not remove colums")
            return
        self.ok("Setting dataframe to columns", " ".join(cols))

    def drop(self, *cols):
        """
        Drops columns from the main dataframe

        :param cols: names of the columns
        :type cols: str

        :example: ``ds.drop("Col 1", "Col 2")``
        """
        try:
            index = self.df.columns.values
            for col in cols:
                if col not in index:
                    self.warning("Column", col, "not found. Aborting")
                    return
                self.df = self.df.drop(col, axis=1)
        except Exception as e:
            self.err(e, self.drop, "Can not drop column")

    def exclude(self, col: str, val):
        """
        Delete rows based on value

        :param col: column name
        :type col: str
        :param val: value to delete
        :type val: any

        :example: ``ds.exclude("Col 1", "value")``
        """
        try:
            self.df = self.df[self.df[col] != val]
        except Exception as e:
            self.err(e, "Can not exclude rows based on value " + str(val))

    def copycol(self, origin_col: str, dest_col: str):
        """
        Copy a columns values in another column

        :param origin_col: name of the column to copy
        :type origin_col: str
        :param dest_col: name of the new column
        :type dest_col: str

        :example: ``ds.copy("col 1", "New col")``
        """
        try:
            self.df[dest_col] = self.df[[origin_col]]
        except Exception as e:
            self.err(e, self.copy_col, "Can not copy column")

    def indexcol(self, col: str):
        """
        Add a column from the index

        :param col: name of the new column
        :type col: str

        :example: ``ds.index_col("New col")``
        """
        try:
            self.df[col] = self.df.index.values
        except Exception as e:
            self.err(e)
            return
        self.ok("Column", col, "added from the index")
