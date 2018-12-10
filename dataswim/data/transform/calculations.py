import pandas as pd
from numpy import nan


class Calculations():
    """
    Class to make calculations on the data
    """

    def diffn(self, diffcol: str, name: str="Diff"):
        """
        Add a diff column to the main dataframe: calculate the diff
        from the next value

        :param diffcol: column to diff from
        :type diffcol: str
        :param name: diff column name, defaults to "Diff"
        :type name: str, optional

        :example: ``ds.diffn("Col 1", "New col")``
        """
        try:
            vals = []
            i = 0
            for _, row in self.df.iterrows():
                current = row[diffcol]
                try:
                    nextv = self.df[diffcol].iloc[i + 1]
                except Exception:
                    vals.append(nan)
                    continue
                val = nextv - current
                vals.append(round(val, 1))
                i += 1
            self.add("Diff", vals)
        except Exception as e:
            self.err(e, self._append, "Can not diff column")
            return
        self.ok("Diff column " + name + " added to the dataframe")

    def diffp(self, diffcol: str, name: str="Diff"):
        """
        Add a diff column to the main dataframe: calculate the diff
        from the previous value

        :param diffcol: column to diff from
        :type diffcol: str
        :param name: diff column name, defaults to "Diff"
        :type name: str, optional

        :example: ``ds.diffp("Col 1", "New col")``
        """
        try:
            df = self.df.copy()
            previous = 0
            i = 0
            vals = [df[diffcol].iloc[0]]
            for _, row in df.iterrows():
                val = row[diffcol] - previous
                new = round(val, 1)
                previous = row[diffcol]
                if i == 0:
                    vals = [0]
                else:
                    vals.append(new)
                i = 1
            self.df = df
            self.add(name, vals)
        except Exception as e:
            self.err(e, self._append, "Can not diff column")
            return
        self.ok("Diff column " + name + " added to the dataframe")

    def diffm(self, diffcol: str, name: str="Diff", default=nan):
        """
        Add a diff column to the main dataframe: calculate the
        diff from the column mean

        :param diffcol: column to diff from
        :type diffcol: str
        :param name: diff column name, defaults to "Diff"
        :param name: str, optional
        :param default: column default value, defaults to nan
        :param default: optional

        :example: ``ds.diffm("Col 1", "New col")``
        """
        try:
            df = self.df.copy()
            mean = self.df[diffcol].mean()
            vals = []
            for _, row in self.df.iterrows():
                num = row[diffcol]
                if num > 0:
                    diff = int(((num - mean) * 100) / mean)
                    vals.append(diff)
                else:
                    vals.append(default)
            self.df = df
            self.add(name, vals)
        except Exception as e:
            self.err(e, self._append, "Can not diff column")
            return
        self.ok("Diff column " + name + " added to the dataframe")

    def diffs(self, col: str, serie: "iterable", name: str="Diff"):
        """
        Add a diff column from a serie. The serie is an iterable
        of the same length than the dataframe

        :param col: column to diff
        :type col: str
        :param serie: serie to diff from
        :type serie: iterable
        :param name: name of the diff col, defaults to "Diff"
        :param name: str, optional

        :example: ``ds.diffs("Col 1", [1, 1, 4], "New col")``
        """
        try:
            d = []
            for i, row in self.df.iterrows():
                v = row[col] - serie[i]
                d.append(v)
            self.df[name] = d
        except Exception as e:
            self.err(e, self._append, "Can not diff column from serie")

    def diffsp(self, col: str, serie: "iterable", name: str="Diff"):
        """
        Add a diff column in percentage from a serie. The serie is 
        an iterable of the same length than the dataframe

        :param col: column to diff
        :type col: str
        :param serie: serie to diff from
        :type serie: iterable
        :param name: name of the diff col, defaults to "Diff"
        :param name: str, optional

        :example: ``ds.diffp("Col 1", [1, 1, 4], "New col")``
        """
        try:
            d = []
            for i, row in self.df.iterrows():
                v = (row[col]*100) / serie[i]
                d.append(v)
            self.df[name] = d
        except Exception as e:
            self.err(e, self._append, "Can not diff column from serie")

    def gmean_(self, col: str, index_col: bool=True) -> "Ds":
        """
        Group by and mean column

        :param col: column to group
        :type col: str
        :param index_col: 
        :type index_col: bool
        :return: a dataswim instance
        :rtype: Ds

        :example: ``ds2 = ds.gmean("Col 1")``
        """
        try:
            df = self.df.copy()
            df = df.groupby([col]).mean()
            if index_col is True:
                df[col] = df.index.values
            return self._duplicate_(df)
        except Exception as e:
            self.err(e, self.gmean_, "Can not meansum column")

    def gsum_(self, col: str, index_col: bool=True) -> "Ds":
        """
        Group by and sum column

        :param col: column to group
        :type col: str
        :param index_col: 
        :type index_col: bool
        :return: a dataswim instance
        :rtype: Ds

        :example: ``ds2 = ds.gsum("Col 1")``
        """
        try:
            df = self.df.copy()
            df = df.groupby([col]).sum()
            if index_col is True:
                df[col] = df.index.values
            return self._duplicate_(df)
        except Exception as e:
            self.err(e, self.gsum_, "Can not groupsum column")

    def ratio(self, col: str, ratio_col: str="Ratio"):
        """
        Add a column whith the percentages ratio from a column

        :param col: column to calculate ratio from
        :type col: str
        :param ratio_col: new ratio column name, defaults to "Ratio"
        :param ratio_col: str, optional

        :example: ``ds2 = ds.ratio("Col 1")``
        """
        try:
            df = self.df.copy()
            df[ratio_col] = df[[col]].apply(
                lambda x: 100 * x / float(x.sum()))
            self.df = df
        except Exception as e:
            self.err(e, self.ratio, "Can not calculate ratio")
