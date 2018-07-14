from goerr.colors import colors


class Search():
    """
    Class to handle searches in the dataframe
    """

    def contains(self, column, value):
        """
        Set the main dataframe instance to rows that contains a string
        value in a column
        """
        df = self._contains(column, value)
        if df is None:
            self.err("Can not select contained data")
            return
        self.df = df

    def contains_(self, column, value):
        """
        Returns a Dataswim instance with rows that contains a string
        value in a column
        """
        df = self._contains(column, value)
        if df is None:
            self.err("Can not select contained data")
            return
        return self._duplicate_(df)

    def _contains(self, column, value):
        try:
            df = self.df[self.df[column].str.contains(value) == True]
            return df
        except Exception as e:
            self.err(e, "Can not select contained data")

    def exact(self, column, *values):
        """
        Sets the main dataframe to rows that has the exact string
        value in a column
        """
        df = self._exact(column, *values)
        if df is None:
            self.err("Can not select exact data")
        self.df = df

    def exact_(self, column, *values):
        """
        Returns a Dataswim instance with rows that has the exact string
        value in a column
        """
        df = self._exact(column, *values)
        if df is None:
            self.err("Can not select exact data")
        return self._duplicate_(df)

    def _exact(self, column, *values):
        try:
            df2 = self.df[column].isin(values)
            df = self.df[df2]
            return df
        except Exception as e:
            self.err(e, "Can not select exact data")
