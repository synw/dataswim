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

    def contains_(self, column, value):
        """
        Returns rows that contains a string value in a column
        """
        try:
            df = self.df[self.df[column].str.contains(value) == True]
            return self.clone_(df.copy())
        except KeyError:
            self.err(self.contains_, "Can not find " +
                     colors.bold(column) + " column")
            return
        except Exception as e:
            self.err(e, self.contains_, "Can not select contained data")

    def exact_(self, column, *values):
        """
        Returns rows that has the exact string value in a column
        """
        try:
            df2 = self.df[column].isin(list(values))
            df = self.df[df2]
            return self.clone_(df)
        except KeyError:
            self.err(self.exact_, "Can not find " +
                     colors.bold(column) + " column")
            return
        except Exception as e:
            self.err(e, self.exact_, "Can not select exact data")
