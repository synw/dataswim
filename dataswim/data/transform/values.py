import pandas as pd
from ..copy import Copy


class Values(Copy):
    """
    A class to transform the dataframe's values
    """

    def sum_(self, col: str) -> float:
        """
        Returns the sum of all values in a column

        :param col: column name
        :type col: str
        :return: sum of all the column values
        :rtype: float

        :example: ``sum = ds.sum_("Col 1")``
        """
        try:
            df = self.df[col]
            num = float(df.sum())
            return num
        except Exception as e:
            self.err(e, "Can not sum data on column " + str(col))

    def dropr(self, *rows):
        """
        Drops some rows from the main dataframe

        :param rows: rows names
        :type rows: list of ints

        :example: ``ds.drop_rows([0, 2])``
        """
        try:
            self.df = rows = list(rows)
            self.df.drop(rows)
        except Exception as e:
            self.err(e, self.dropr, "Can not drop rows")

    def append(self, vals: list, index=None):
        """
        Append a row to the main dataframe

        :param vals: list of the row values to add
        :type vals: list
        :param index: index key, defaults to None
        :param index: any, optional

        :example: ``ds.append([0, 2, 2, 3, 4])``
        """
        try:
            # self.df.append(vals)
            self.df.append(pd.DataFrame(columns=self.df.columns, data=[vals]))
        except Exception as e:
            self.err(e, self.append, "Can not append row")
            return
        self.ok("Row added to dataframe")

    def sort(self, col: str):
        """
        Sorts the main dataframe according to the given column

        :param col: column name
        :type col: str

        :example: ``ds.sort("Col 1")``
        """
        try:
            self.df = self.df.copy().sort_values(col)
        except Exception as e:
            self.err(e, "Can not sort the dataframe from column " +
                     str(col))

    def reverse(self):
        """
        Reverses the main dataframe order

        :example: ``ds.reverse()``
        """
        try:
            self.df = self.df.iloc[::-1]
        except Exception as e:
            self.err(e, "Can not reverse the dataframe")

    def apply(self, function: "function", *cols, axis=1, **kwargs):
        """
        Apply a function on columns values

        :param function: a function to apply to the columns
        :type function: function
        :param cols: columns names
        :type cols: name of columns
        :param axis: index (0) or column (1), default is 1
        :param kwargs: arguments for ``df.apply``
        :type kwargs: optional

        :example:
                        .. code-block:: python

                                def f(row):
                                        # add a new column with a value
                                        row["newcol"] = row["Col 1] + 1
                                        return row

                                ds.apply(f)

        """
        try:
            if len(cols) == 0:
                self.df = self.df.apply(function, axis=axis, **kwargs)
            else:
                cols = list(cols)
                self.df[cols] = self.df[cols].apply(function, **kwargs)
        except Exception as e:
            self.err(e, "Can not apply function")

    def pivot(self, index, **kwargs):
        """
        Pivots a dataframe
        """
        try:
            return pd.pivot_table(self.df, index=kwargs["index"],  **kwargs)
            """if df is None:
                self.err("Can not pivot table")
                return
            self.df = df"""
        except Exception as e:
            self.err(e, "Can not pivot dataframe")

    def trimquants(self, col: str, inf: float, sup: float):
        """
        Remove superior and inferior quantiles from the dataframe

        :param col: column name
        :type col: str
        :param inf: inferior quantile
        :type inf: float
        :param sup: superior quantile
        :type sup: float

        :example: ``ds.trimquants("Col 1", 0.01, 0.99)``
        """
        try:
            self.df = self._trimquants(col, inf, sup)
        except Exception as e:
            self.err(e, self.trimquants, "Can not trim quantiles")

    def trimsquants(self, col: str, sup: float):
        """
        Remove superior quantiles from the dataframe

        :param col: column name
        :type col: str
        :param sup: superior quantile
        :type sup: float

        :example: ``ds.trimsquants("Col 1", 0.99)``
        """
        try:
            self.df = self._trimquants(col, None, sup)
        except Exception as e:
            self.err(e, self.trimsquants, "Can not trim superior quantiles")

    def trimiquants(self, col: str, inf: float):
        """
        Remove superior and inferior quantiles from the dataframe

        :param col: column name
        :type col: str
        :param inf: inferior quantile
        :type inf: float

        :example: ``ds.trimiquants("Col 1", 0.05)``
        """
        try:
            self.df = self._trimquants(col, inf, None)
        except Exception as e:
            self.err(e, self.trimiquants, "Can not trim inferior quantiles")

    def _trimquants(self, col, inf, sup):
        try:
            ds2 = self._duplicate_()
            if inf is not None:
                qi = ds2.df[col].quantile(inf)
                ds2.df = ds2.df[ds2.df[col] > qi]
            if sup is not None:
                qs = ds2.df[col].quantile(sup)
                ds2.df = ds2.df[ds2.df[col] < qs]
        except Exception as e:
            self.err(e, self._trimquants, "Can not trim quantiles")
            return
        msg = "Removed values "
        if inf is not None:
            msg += "under " + str(qi)
        if sup is not None and inf is not None:
            msg += " and"
        if sup is not None:
            msg += "upper " + str(qs)
        self.ok(msg, "in column", col)
        return ds2.df
