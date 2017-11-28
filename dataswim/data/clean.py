# -*- coding: utf-8 -*-

import time
import pandas as pd
from numpy.core.numeric import nan
from goerr.colors import colors


class Clean():
    """
    Class to clean the data
    """

    def drop_nan(self, field=None, method="all"):
        """
        Drop NaN values from the main dataframe
        """
        try:
            if field is None:
                self.df = self.df.dropna(how=method)
            else:
                self.df = self.df[self.df[field].notnull()]
        except Exception as e:
            self.err(e, self.drop_nan, "Error droping nan values")

    def nan_empty(self, field):
        """
        Fill empty values with NaN values
        """
        try:
            self.df[field] = self.df[field].replace('', nan)
        except Exception as e:
            self.err(e, self.nan_empty_, "Can not fill empty values with nan")

    def zero_nan(self, *fields):
        """
        Converts zero values to nan values in selected columns
        """
        try:
            self.df = self._zero_nan(*fields)
        except Exception as e:
            self.err(e, self.nan_empty_, "Can not fill zero values with nan")

    def zero_nan_(self, *fields):
        """
        Returns a DataSwim instance with zero values to nan values in selected columns
        """
        df = self.clone_(self._zero_nan(*fields))
        return self.clone_(df)

    def _zero_nan(self, *fields):
        """
        Converts zero values to nan values in selected columns
        """
        df = self.df.copy()
        try:
            for field in fields:
                df = df.replace({field: {nan: 0}})
            if self.autoprint is True:
                s = "s"
                if len(fields) == 1:
                    s = ""
                self.ok("Replaced 0 values by nan in column" + s, field)
            return df
        except Exception as e:
            self.err(e)

    def fill_nan(self, val, *fields):
        """
        Fill NaN values with new values
        """
        try:
            self.df = self._fill_nan(val, *fields)
        except Exception as e:
            self.err(e, self.fill_nan, "Can not fill nan values")

    def fill_nan_(self, val, *fields):
        """
        Returns a DataSwim instance with NaN values filled
        """
        fields = list(fields)
        if len(fields) == 0:
            fields = self.df.index.values
        try:
            df = self._fill_nan(val, *fields)
            return self.clone_(df=df)
        except Exception as e:
            self.err(e, self.fill_nan_, "Can not fill nan values")

    def _fill_nan(self, val, *fields):
        """
        Fill NaN values with new values
        """
        fields = list(fields)
        df = self.df.copy()
        try:
            for el in fields:
                try:
                    df[el] = df[[el]].fillna(val)
                except KeyError:
                    self.warning("Can not find column ", el)
                    return
        except Exception as e:
            self.err(e, self._fill_nan, "Can not fill nan values")
        if self.autoprint is True:
            self.ok("Filled nan values in columns", *fields)
        return df

    def fill_nulls(self, field):
        """
        Fill all null values with NaN values
        """
        n = [None, ""]
        try:
            self.df[field] = self.df[field].replace(n, nan)
        except Exception as e:
            self.err(e)

    def to_int(self, field):
        """
        Convert some column values to integers
        """
        """
        for field in fields:
            self.drop_nan(field)
            self.df[field] = self.df[field].dropna().astype(int)

        """
        ds2 = self.clone_()
        try:
            ds2.drop_nan(field, method="any")
            ds2.df[field] = ds2.df[field].apply(lambda x: int(x))
            self.df = ds2.df
        except Exception as e:
            self.err(e, self.to_int, "Can not convert column values to integer")
            return
        if self.autoprint is True:
            self.ok("Converted column values to integers")

    def to_float(self, *cols):
        """
        Convert colums values to float
        """
        try:
            df = self._to_type("float64", *cols)
            self.df = df
        except Exception as e:
            self.err(e, self._to_type, "Can not convert column values to float")
            return
        if self.autoprint is True:
            self.ok("Converted column values to float")

    def _to_type(self, dtype, *cols):
        """
        Convert colums values to a given type
        """
        df = self.df.copy()
        allcols = df.columns.values
        try:
            for col in cols:
                if col not in allcols:
                    self.err(self._to_type, "Column " + col + " not found")
                    return
                df[col] = df[col].astype(dtype)
            return df
        except Exception as e:
            self.err(e)

    def clean_ts(self, date_col, numeric_col=None, index=True, to_int=False, index_col=True):
        """
        Cleans and format a timeseries dataframe
        """
        try:
            self.date(date_col)
            if index is True:
                self.dateindex(date_col)
            if numeric_col is not None:
                self.fill_nan(numeric_col)
                if to_int is True:
                    self.to_int(numeric_col)
            if index_col is True:
                self.index_col()
            self.index_col(date_col)
        except Exception as e:
            self.err(e)

    def date(self, *fields):
        """
        Convert column values to properly formated datetime
        """
        def convert(row):
            try:
                t1 = row.timetuple()
                int(time.mktime(t1))
            except:
                return nan
            return row.strftime('%Y-%m-%d %H:%M:%S')

        try:
            for f in fields:
                try:
                    df2 = self.df.copy()
                    self.df[f] = pd.to_datetime(df2[f]).apply(convert)
                except ValueError:
                    pass
        except KeyError:
            self.warning("Can not find colums " + " ".join(fields))
            return
        except Exception as e:
            self.err(e, self.date, "Can not process date field")

    def dateindex(self, datafield, indexfield="date_index", df=None):
        """
        Set a datetime index from a column
        """
        try:
            self.df = self._dateindex(datafield, indexfield, df)
        except Exception as e:
            self.err(e, self.dateindex, "Can not index data")

    def dateindex_(self, datafield, indexfield="date_index", df=None):
        """
        Returns a DataSwim instance index from a column
        """
        try:
            df = self._dateindex(datafield, indexfield, df)
        except Exception as e:
            self.err(e, self.dateindex_, "Can not index data")
            return
        return self.clone_(df=df)

    def _dateindex(self, datafield, indexfield, df=None):
        """
        Returns a datetime index from a column
        """
        if df is None:
            df = self.df.copy()
        try:
            index = pd.DatetimeIndex(df[datafield])
            df = df.set_index(index)
        except KeyError as e:
            self.err(e, self._dateindex, "Can not find column " +
                     colors.bold(datafield) + " in data")
            return
        except Exception as e:
            msg = "Can not reindex with datafield " + \
                colors.bold(datafield) + " and indexfield " + \
                colors.bold(indexfield)
            self.err(e, self._dateindex, msg)
            return
        if self.autoprint is True:
            self.ok("Added a datetime index from column", datafield)
        return df

    def format_date_(self, date):
        """
        Formats a date
        """
        return date.strftime('%Y-%m-%d %H:%M:%S')

    def transform_(self, dateindex=None, index_col=None, fill_col=None, num_col=None, df=None):
        """
        Returns a DataSwim instance transformed according to the given parameters
        """
        if df is None:
            if self.df is None:
                self.err(
                    self._transform, "No dataframe: please provide one in parameters or set it")
                return
            df = self.df.copy()
        ds2 = self.clone_(df)
        if dateindex is None and index_col is None and fill_col is None and num_col is None:
            return ds2
        try:
            if dateindex is not None:
                ds2 = ds2.dateindex_(dateindex, df=df)
            if fill_col is not None:
                ds2 = ds2.fill_nan_(0, fill_col)
            if index_col is not None:
                ds2 = ds2.index_col_(index_col)
            if num_col is not None:
                ds2.add(num_col, 1)
            return ds2
        except Exception as e:
            self.err(e, self.transform_, "Can not transform data")
