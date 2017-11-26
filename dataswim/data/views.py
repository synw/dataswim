# -*- coding: utf-8 -*-

import pandas as pd
from pandas_profiling import ProfileReport
from goerr.colors import colors


class View():
    """
    Class to view the data
    """

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df

    def head(self, rows=5):
        """
        Returns the main dataframe's head
        """
        if self.df is None:
            self.warning("Dataframe is empty: no head available")
            return
        return self.df.head(rows)

    def tail(self, rows=5):
        """
        Returns the main dataframe's tail
        """
        if self.df is None:
            self.warning("Dataframe is empty: no tail available")
        return self.df.tail(rows)

    def look(self, df=None, p=True):
        """
        Returns basic data info
        """
        if df is None:
            df = self.df
        if df is None:
            self.warning("Dataframe is empty: nothing to look at")
            return
        num = len(self.df.index)
        if p is True:
            print(num, "rows")
            print("Fields:", ", ".join(list(self.df)))
        else:
            return p

    def describe(self):
        """
        Return a description of the data
        """
        if self.df is None:
            self.warning("Dataframe is empty: nothing to describe")
            return
        self.look()
        return self.df.describe()

    def show(self, rows=5, dataframe=None):
        """
        Display info about a dataframe
        """
        try:
            if dataframe is not None:
                df = dataframe
            else:
                df = self.df
            if df is None:
                self.warning("Dataframe is empty: nothing to show")
                return
            num = len(df.index)
        except Exception as e:
            self.err(e, self.show, "Can not show dataframe")
            return
        f = list(df)
        num_fields = len(f)
        fds = []
        for fi in f:
            fds.append(str(fi))
        fields = ", ".join(fds)
        if self.autoprint is True:
            self.info("The dataframe has", colors.bold(num), "rows and",
                      colors.bold(num_fields), "columns:")
            print(fields)
        return df.head(rows)

    def report(self, df=None):
        """
        Returns a dataframe profiling report
        """
        if df is None:
            df = self.df
        if self.df is None:
            self.warning("Dataframe is empty: nothing to report")
            return
        return ProfileReport(df)

    def display(self, *fields):
        """
        Display some columns head
        """
        try:
            if self.df is None:
                self.warning("Dataframe is empty: nothing to display")
                return
            df2 = self.df[list(fields)]
            return df2.head()
        except Exception as e:
            self.err(e, self.display, "Can not display dataframe")

    def types_(self, col):
        """
        Display types of values in a column
        """
        df = self.df.copy()
        cols = df.columns.values
        all_types = {}
        for col in cols:
            local_types = []
            for i, val in self.df[col].iteritems():
                #print(i, val, type(val))
                t = type(val).__name__
                if t not in local_types:
                    local_types.append(t)
            all_types[col] = (local_types, i)
        df = pd.DataFrame(all_types, index=["type", "num"])
        return self.clone_(df)

    def cols(self):
        """
        Prints columns info
        """
        try:
            df = self._cols()
            return df.head(100)
        except Exception as e:
            self.err(e, self._cols, "Can not display column infos")

    def cols_(self):
        """
        Returns a DataSwim instance with columns info
        """
        try:
            df = self._cols()
            return self.clone_(df)
        except Exception as e:
            self.err(e, self._cols, "Can not display column infos")

    def _cols(self):
        """
        Returns a dataframe with columns info
        """
        try:
            df = self.df.copy()
            s = df.iloc[0]
            df = pd.DataFrame(s)
            df = df.rename(columns={0: "value"})

            # TODO : revert columns value and type order
            #cols = df.columns.tolist()
            #cols = cols[-1:] + cols[:-1]
            #df = df[cols]

            def run(row):
                t = row[0]
                return type(t).__name__

            s = df.apply(run, axis=1)
            df = df.rename(columns={0: "value"})
            df["type"] = s
            return df
        except Exception as e:
            self.err(e)

    def vals(self, field):
        """
        Set the main dataframe to the values count of a column     
        """
        self.df = self._vals(field)

    def vals_(self, field, index_col="index"):
        """
        Returns a DatasWim instance from values count of a column     
        """
        ds2 = self.clone_(df=self._vals(field))
        ds2.index_col(index_col)
        return ds2

    def _vals(self, field):
        """
        Returns a DatasWim instance from values count of a column     
        """
        if self.df is None:
            self.warning("Dataframe is empty: no values to show")
            return
        count = self.df[field].value_counts()
        df = pd.DataFrame(count)
        return df
