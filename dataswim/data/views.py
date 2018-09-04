import pandas as pd
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
            num = len(df.columns.values)
        except Exception as e:
            self.err(e, self.show, "Can not show dataframe")
            return
        f = list(df)
        fds = []
        for fi in f:
            fds.append(str(fi))
        fields = ", ".join(fds)
        num_rows = len(df.index)
        self.info("The dataframe has", colors.bold(num_rows), "rows and",
                  colors.bold(num), "columns:")
        print(fields)
        return df.head(rows)

    def one(self):
        """
        Shows one row of the main dataframe and the field names wiht count
        """
        try:
            return self.show(1)
        except Exception as e:
            self.err(e, self.one, "Can not display dataframe")

    def title(self, txt):
        """
        Prints a title for pipelines
        """
        num = len(txt)
        ticks = "=" * num
        print(ticks)
        print(txt)
        print(ticks)

    def subtitle(self, txt):
        """
        Prints a subtitle for pipelines
        """
        num = len(txt)
        ticks = "-" * num
        print(txt)
        print(ticks)

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

    def cols(self, limit=100):
        """
        Prints columns info
        """
        try:
            df = self._cols()
            return df.head(limit)
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

    def vals(self, col, num=15, index_col=None, num_col="Number"):
        """
        Print the values count of a column
        """
        df = self._vals(col, num_col)
        ds = self.new_(df)
        if index_col is None:
            index_col = col
        ds.index_col(index_col)
        return ds.show(num)

    def vals_(self, col, index_col=None, num_col="Number"):
        """
        Returns a DatasWim instance from values count of a column
        """
        ds = self.clone_(self._vals(col, num_col))
        self.quiet = True
        if index_col is None:
            index_col = col
        ds.index_col(index_col)
        self.quiet = False
        return ds

    def _vals(self, col, num_col):
        """
        Returns a DatasWim instance from values count of a column
        """
        if self.df is None:
            self.warning("Dataframe is empty: no values to show")
            return
        count = self.df[col].value_counts()
        df = pd.DataFrame(count)
        df = df.rename(columns={col: num_col})
        return df
