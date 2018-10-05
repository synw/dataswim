# @PydevCodeAnalysisIgnore
import pandas as pd
from numpy import nan


class Transform():
    """
    Class to transform data
    """

    def keep_(self, *fields):
        """
        Limit a dataframe to some columns
        """
        try:
            ds2 = self._duplicate_(self.df[list(fields)])
        except Exception as e:
            self.err(e, "Can not remove colums")
            return
        self.ok("Columns", " ,".join(fields), "kept")
        return ds2

    def keep(self, *fields):
        """
        Limit a dataframe to some columns
        """
        try:
            self.df = self.df[list(fields)]
        except Exception as e:
            self.err(e, "Can not remove colums")
            return
        self.ok("Setting dataframe to columns", " ".join(fields))

    def drop(self, *cols):
        """
        Drops columns from the main dataframe
        """
        try:
            index = self.df.columns.values
            for col in cols:
                if col not in index:
                    self.warning("Column", col, "not found. Aborting")
                    return
                for col in cols:
                    self.df = self.df.drop(col, axis=1)
        except Exception as e:
            self.err(e, self.drop, "Can not drop column")

    def exclude(self, col, val):
        """
        Delete rows based on value
        """
        try:
            self.df = self.df[self.df[col] != val]
        except Exception as e:
            self.err(e, "Can not exclude rows based on value " + str(val))

    def rsum(self, time_period="1Min", num_col="Number",
             dateindex=None, index_col="Date", fill_col=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        df = self._resample_("sum", time_period,
                                     num_col, dateindex, index_col, fill_col)
        if df is None:
            self.err("Can not sum data")
            return
        self.df = df

    def rsum_(self, time_period="1Min", num_col="Number",
              dateindex=None, index_col="Date", fill_col=None):
        """
        Resample, and sum a dataframe to a time period
        """
        df = self._resample_("sum", time_period,
                            num_col, dateindex, index_col, fill_col)
        if df is None:
            self.err("Can not sum data")
            return
        return self._duplicate_(df)

    def _resample_(self, method, time_period, num_col,
                  dateindex, index_col, fill_col):
        try:
            ds2 = self._duplicate_()
            if dateindex is not None:
                ds2 = self.dateindex_(dateindex)
                if ds2 is None:
                    self.err("Can not process date index")
                    return
            if num_col is not None:
                ds2.add(num_col, 1)
            ds2.df = ds2.df.resample(time_period)
            if method == "sum":
                ds2.df = ds2.df.sum()
            elif method == "mean":
                if num_col is not None:
                    num_vals = ds2.df[num_col].sum()
                ds2.df = ds2.df.mean()
                ds2.df[num_col] = num_vals
            else:
                self.err("Resampling method " + method + " unknown")
                return
            self.ok("Data resampled by", time_period)
            ds2 = self.transform_(None, index_col,
                                 fill_col, None, df=ds2.df)
            df = ds2.df
            if df is None:
                self.err("Can not transform data after resampling")
                return
            return df
        except Exception as e:
            self.err(e, "Can not resample data")
            return

    def rmean(self, time_period="1Min", num_col="Number",
              dateindex=None, index_col="Date", fill_col=None):
        """
        Resample, and sum the main dataframe to a time period
        """
        df = self._resample_("mean", time_period,
                            num_col, dateindex, index_col, fill_col)
        if df is None:
            self.err("Can not mean data")
            return
        self.df = df

    def rmean_(self, time_period="1Min", num_col="Number",
               dateindex=None, index_col="Date", fill_col=None):
        """
        Resample, and sum a dataframe to a time period
        """
        df = self._resample_("mean", time_period,
                            num_col, dateindex, index_col, fill_col)
        if df is None:
            self.err("Can not mean data")
            return
        return self._duplicate_(df)

    def sum_(self, column):
        """
        Returns the sum of all values in a column
        """
        try:
            df = self.df[column]
            num = df.sum()
            return num
        except Exception as e:
            self.err(e, "Can not sum data on column " + str(column))

    def reverse(self):
        """
        Reverses the main dataframe order
        """
        try:
            self.df = self.df.iloc[::-1]
        except Exception as e:
            self.err(e, "Can not reverse the dataframe")

    def sort(self, column):
        """
        Sorts the main dataframe according to the given column
        """
        try:
            self.df = self.df.copy().sort_values(column)
        except Exception as e:
            self.err(e, "Can not sort the dataframe from column " + 
                     str(column))

    def apply(self, function, *cols, **kwargs):
        """
        Apply a function on columns values
        """
        try:
            if len(cols) == 0:
                self.df = self.df.apply(function, **kwargs)
            else:
                cols = list(cols)
                self.df[cols] = self.df[cols].apply(function, **kwargs)
        except Exception as e:
            self.err(e, "Can not apply function")

    def replace(self, col, origin, dest, **kwargs):
        """
        Replace a value in a column
        """
        try:
            self.df[col] = self.df[col].replace(origin, dest)
        except Exception as e:
            self.err(e, "Can not replace value")
            return
        self.ok("Replaced value in column " + str(col))

    def pivot(self, index, **kwargs):
        """
        Pivots a dataframe
        """
        df = self._pivot(index, **kwargs)
        if df is None:
            self.err("Can not pivot table")
            return
        self.df = df

    def pivot_(self, index, **kwargs):
        """
        Pivots a dataframe
        """
        df = self._pivot(index, **kwargs)
        if df is None:
            self.err("Can not pivot table")
            return
        return self._duplicate_(df)

    def _pivot(self, index, **kwargs):
        try:
            kwargs["index"] = index
            return pd.pivot_table(self.df, **kwargs)
        except Exception as e:
            self.err(e, "Can not pivot table")

    def concat(self, *dss, **kwargs):
        """
        Concatenate instances from a list and set it to the main dataframe
        """
        df = self._concat(*dss, **kwargs)
        if df is None:
            self.err("Can not concatenate data")
            return
        self.df = df

    def concat_(self, *dss, **kwargs):
        """
        Concatenate dataframes from a list and returns a new DataSwim instance
        """
        df = self._concat(*dss, **kwargs)
        if df is None:
            self.err("Can not concatenate data")
            return
        return self._duplicate_(df)

    def _concat(self, *dss, **kwargs):
        try:
            df = pd.DataFrame()
            for dsx in dss:
                df = pd.concat([df, dsx.df], **kwargs)
            return df
        except Exception as e:
            self.err(e, "Can not concatenate data")

    def split_(self, col):
        """
        Split the main dataframe according to a column's unique values and
        return a dict of dataswim instances
        """
        try:
            dss = {}
            unique = self.df[col].unique()
            for key in unique:
                df2 = self.df.loc[self.df[col] == key]
                ds2 = self._duplicate_(df2)
                dss[key] = ds2
            return dss
        except Exception as e:
            self.err(e, "Can not split dataframe")

    def add(self, column, value):
        """
        Add a columns with default values
        """
        try:
            df = self.df.copy()
            df[column] = value
            self.df = df
        except Exception as e:
            self.err(e, self.add, "Can not add column")

    def copy_col(self, origin_col, end_col):
        """
        Copy a columns values in another column
        """
        try:
            df = self.df.copy()
            df[end_col] = df[[origin_col]]
            self.df = df
        except Exception as e:
            self.err(e, self.copy_col, "Can not copy column")

    def index_col(self, column="index"):
        """
        Add a column filled from the index to the main dataframe
        """
        try:
            self.df = self._index_col(column)
        except Exception as e:
            self.err(e, self.index_col, "Can not add index column")

    def index_col_(self, column="index"):
        """
        Returns a DatasWim instance with a new column filled from the index
        """
        try:
            df = self._index_col(column)
            return self.df
        except Exception as e:
            self.err(e, self.index_col_, "Can not add index column")

    def _index_col(self, column):
        """
        Add a column from the index
        """
        df = self.df.copy()
        try:
            df[column] = df.index.values
            if self.autoprint is True:
                self.ok("Column", column, "added from index")
            return df
        except Exception as e:
            self.err(e)

    def drop_rows(self, *rows):
        """
        Drops some rows from the main dataframe
        """
        try:
            self.df = self._drop_rows(rows)
        except Exception as e:
            self.err(e, self.drop_rows, "Can not drop rows")
            return

    def _drop_rows(self, rows):
        """
        Drops some rows from the main dataframe
        """
        try:
            df = self.df.copy()
            rows = list(rows)
            df = df.drop(rows)
            return df
        except Exception as e:
            self.err(e, self._drop_rows, "Can not drop rows")
            return
        if self.autoprint is True:
            self.ok("Dropped rows", ", ".join(rows))

    def append(self, vals, index=None):
        """
        Append a row to the main dataframe
        """
        try:
            self.df = self._append(vals, index)
        except Exception as e:
            self.err(e, self.append, "Can not append row")
            return

    def append_(self, vals, index=None):
        """
        Returns a dataswim instance with one more row
        """
        try:
            return self.duplicate_(self._append(vals, index))
        except Exception as e:
            self.err(e, self.append_, "Can not append row")
            return

    def _append(self, vals, index):
        """
        Returns a dataframe with a new row
        """
        try:
            df = self.df.copy()
            if index is None:
                index = len(df)
            df.loc[index] = vals
            return df
        except Exception as e:
            self.err(e, self._append, "Can not append row")
            return
        if self.autoprint is True:
            self.ok("Row added to dataframe")

    def merge(self, df, on, how="outer", **kwargs):
        """
        Set the main dataframe from the current dataframe and the passed
        dataframe
        """
        try:
            df = self._merge(df, on, how, **kwargs)
            self.df = df
        except Exception as e:
            self.err(e, self.merge, "Can not merge dataframes")

    def merge_(self, df, on, how="outer", **kwargs):
        """
        Returns a Dataswim instance from the current dataframe and the passed
        dataframe
        """
        try:
            df = self._merge(df, on, how, **kwargs)
            ds = self.clone_(df)
            return ds
        except Exception as e:
            self.err(e, self.merge_, "Can not merge dataframes")

    def _merge(self, df, on, how, **kwargs):
        """
        Returns a dataframe from the current dataframe and the passed
        dataframe
        """
        try:
            df = pd.merge(self.df, df, on=on, how=how, **kwargs)
            return df
        except Exception as e:
            self.err(e, self._merge, "Can not merge dataframes")

    def diffn(self, diffcol, name="Diff"):
        """
        Add a diff column to the main dataframe
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
        if self.autoprint is True:
            self.ok("Diff column " + name + " added to the dataframe")

    def diff(self, diffcol, name="Diff"):
        """
        Add a diff column to the main dataframe
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
        if self.autoprint is True:
            self.ok("Diff column " + name + " added to the dataframe")

    def diffm(self, diffcol, name="Diff", default=nan):
        """
        Add a diff from mean column to the main dataframe
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
        if self.autoprint is True:
            self.ok("Diff column " + name + " added to the dataframe")

    def gmean_(self, col, index_col=True):
        """
        Group by and mean column
        """
        try:
            df = self.df.copy()
            df = df.groupby([col]).mean()
            if index_col is True:
                df[col] = df.index.values
            return self.clone_(df)
        except Exception as e:
            self.err(e, self.gmean_, "Can not meansum column")

    def gsum_(self, col, index_col=True):
        """
        Group by and sum column
        """
        try:
            df = self.df.copy()
            df = df.groupby([col]).sum()
            if index_col is True:
                df[col] = df.index.values
            return self.clone_(df)
        except Exception as e:
            self.err(e, self.gsum_, "Can not groupsum column")

    def ratio(self, col, ratio_col="Ratio"):
        """
        Add a column whith the percentages ratio from a column
        """
        try:
            df = self.df.copy()
            df[ratio_col] = df[[col]].apply(
                lambda x: 100 * x / float(x.sum()))
            self.df = df
        except Exception as e:
            self.err(e, self.ratio, "Can not calculate ratio")

    def rename(self, source_col, dest_col):
        """
        Renames a column in the main dataframe
        """
        try:
            self.df = self.df.rename(columns={source_col: dest_col})
        except Exception as e:
            self.err(e, self.rename, "Can not rename column")
            return
        if self.autoprint is True:
            self.ok("Column", source_col, "renamed")

    def trimquants_(self, col, inf, sup):
        """
        Remove superior and inferior quantiles from the dataframe and
        returns a Dataswim instance
        """
        try:
            ds2 = self.clone_()
            ds2.df = self._trimquants(col, inf, sup)
            return ds2
        except Exception as e:
            self.err(e, self.trimquants_, "Can not trim quantiles")

    def trimquants(self, col, inf, sup):
        """
        Remove superior and inferior quantiles from the dataframe
        """
        try:
            self.df = self._trimquants(col, inf, sup)
        except Exception as e:
            self.err(e, self.trimquants, "Can not trim quantiles")

    def trimsquants(self, col, sup):
        """
        Remove superior quantiles from the dataframe
        """
        try:
            self.df = self._trimquants(col, None, sup)
        except Exception as e:
            self.err(e, self.trimsquants, "Can not trim superior quantiles")

    def trimiquants(self, col, inf):
        """
        Remove superior and inferior quantiles from the dataframe
        """
        try:
            self.df = self._trimquants(col, inf, None)
        except Exception as e:
            self.err(e, self.trimiquants, "Can not trim inferior quantiles")

    def _trimquants(self, col, inf, sup):
        """
        Remove superior and inferior quantiles from the dataframe
        and returs a dataframe
        """
        try:
            ds2 = self.clone_()
            if inf is not None:
                qi = ds2.df[col].quantile(inf)
                ds2.df = ds2.df[ds2.df[col] > qi]
            if sup is not None:
                qs = ds2.df[col].quantile(sup)
                ds2.df = ds2.df[ds2.df[col] < qs]

        except Exception as e:
            self.err(e, self._trimquants, "Can not trim quantiles")
        if self.autoprint is True:
            msg = "Removed values "
            if inf is not None:
                msg += "under " + str(qi)
            if sup is not None and inf is not None:
                msg += " and"
            if sup is not None:
                msg += "upper " + str(qs)
            self.ok(msg, "in column", col)
        return ds2.df

    def transform_(self, dateindex=None, index_col=None,
                   fill_col=None, num_col=None, df=None):
        """
        Returns a DataSwim instance transformed according to the
        given parameters
        """
        if df is None:
            if self.df is None:
                self.err("No dataframe: please provide one "
                         "in parameters or set it")
                return
            df = self.df
        ds2 = self._duplicate_(df)
        if dateindex is None and index_col is None and fill_col \
                is None and num_col is None:
            return ds2
        try:
            if dateindex is not None:
                ds2.dateindex(dateindex, df=df)
            if fill_col is not None:
                ds2.fill_nan(0, fill_col)
            if index_col is not None:
                ds2.index_col(index_col)
            if num_col is not None:
                ds2.add(num_col, 1)
            return ds2
        except Exception as e:
            self.err(e, "Can not transform data")
