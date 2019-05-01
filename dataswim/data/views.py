import pandas as pd
from goerr.colors import colors
from .copy import Copy


class View(Copy):
    """
    Class to view the data
    """

    def show(self, rows: int=5,
             dataframe: pd.DataFrame=None) -> pd.DataFrame:
        """
        Display info about the dataframe

        :param rows: number of rows to show, defaults to 5
        :param rows: int, optional
        :param dataframe: a pandas dataframe, defaults to None
        :param dataframe: pd.DataFrame, optional
        :return: a pandas dataframe
        :rtype: pd.DataFrame

        :example: ``ds.show()``
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
        Shows one row of the dataframe and the field 
        names wiht count

        :return: a pandas dataframe
        :rtype: pd.DataFrame

        :example: ``ds.one()``
        """
        try:
            return self.show(1)
        except Exception as e:
            self.err(e, self.one, "Can not display dataframe")

    def tail(self, rows: int=5):
        """
        Returns the main dataframe's tail

        :param rows: number of rows to print, defaults to 5
        :param rows: int, optional
        :return: a pandas dataframe
        :rtype: pd.DataFrame

        :example: ``ds.tail()``
        """
        if self.df is None:
            self.warning("Dataframe is empty: no tail available")
        return self.df.tail(rows)

    def cols_(self) -> pd.DataFrame:
        """
        Returns a dataframe with columns info

        :return: a pandas dataframe
        :rtype: pd.DataFrame

        :example: ``ds.cols_()``
        """
        try:
            s = self.df.iloc[0]
            df = pd.DataFrame(s)
            df = df.rename(columns={0: "value"})

            def run(row):
                t = row[0]
                return type(t).__name__

            s = df.apply(run, axis=1)
            df = df.rename(columns={0: "value"})
            df["types"] = s
            return df
        except Exception as e:
            self.err(e)

    def describe_(self):
        """
        Return a description of the data

        :return: a pandas dataframe
        :rtype: pd.DataFrame

        :example: ``ds.describe()``
        """
        if self.df is None:
            self.warning("Dataframe is empty: nothing to describe")
            return
        return self.df.describe()

    def types_(self, col: str) -> pd.DataFrame:
        """
        Display types of values in a column

        :param col: column name
        :type col: str
        :return: a pandas dataframe
        :rtype: pd.DataFrame

        :example: ``ds.types_("Col 1")``
        """
        cols = self.df.columns.values
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
        return df
