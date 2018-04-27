from goerr.colors import colors


class Search():
    """
    Class to handle searches in the dataframe
    """

    def __init__(self, df=None, db=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df

    def contains(self, column, value):
        """
        Set the main dataframe instance to rows that contains a string
        value in a column
        """
        try:
            df = self._contains(column, value)
            self.df = df
        except KeyError:
            self.err(self.contains, "Can not find " +
                     colors.bold(column) + " column")
            return
        except Exception as e:
            self.err(e, self.contains, "Can not select contained data")

    def contains_(self, column, value):
        """
        Returns a Dataswim instance with rows that contains a string
        value in a column
        """
        try:
            df = self._contains(column, value)
            return self.clone_(df.copy())
        except KeyError:
            self.err(self.contains_, "Can not find " +
                     colors.bold(column) + " column")
            return
        except Exception as e:
            self.err(e, self.contains_, "Can not select contained data")

    def _contains(self, column, value):
        """
        Returns a dataframe with rows that contains a string value in a column
        """
        try:
            df = self.df[self.df[column].str.contains(value) == True]
            return df
        except KeyError:
            self.err(self._contains, "Can not find " +
                     colors.bold(column) + " column")
            return
        except Exception as e:
            self.err(e, self._contains, "Can not select contained data")

    def exact(self, column, *values):
        """
        Sets the main dataframe to rows that has the exact string
        value in a column
        """
        try:
            df = self._exact(column, *values)
            self.df = df
        except KeyError:
            self.err(self.exact, "Can not find " +
                     colors.bold(column) + " column")
            return
        except Exception as e:
            self.err(e, self.exact, "Can not select exact data")

    def exact_(self, column, *values):
        """
        Returns a Dataswim instance with rows that has the exact string
        value in a column
        """
        try:
            df = self._exact(column, *values)
            return self.clone_(df)
        except KeyError:
            self.err(self.exact_, "Can not find " +
                     colors.bold(column) + " column")
            return
        except Exception as e:
            self.err(e, self.exact_, "Can not select exact data")

    def _exact(self, column, *values):
        """
        Returns rows that has the exact string value in a column
        """
        try:
            df2 = self.df[column].isin(values)
            df = self.df[df2]
            return df
        except KeyError:
            self.err(self._exact_, "Can not find " +
                     colors.bold(column) + " column")
            return
        except Exception as e:
            self.err(e, self._exact_, "Can not select exact data")
