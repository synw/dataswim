# -*- coding: utf-8 -*-

import time
import pandas as pd
from numpy.core.numeric import nan


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
                self.df[field] = self.df[field].dropna()
        except Exception as e:
            self.err(e, self.drop_nan, "Error droping nan values")

    def nan_empty(self, field):
        """
        Fill empty values with NaN values
        """
        try:
            self.df[field] = self.df[field].replace('', NaN)
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
            return self.duplicate(df=df)
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
                df[el] = df[[el]].fillna(val)
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
            self.df[field] = self.df[field].replace(n, NaN)
        except Exception as e:
            self.err(e)

    def clean_ts(self, date_col, numeric_col=None, index=True, to_int=False, index_col=True):
        """
        Cleans and format a timeseries dataframe
        """
        try:
            self.date(date_col)
            if index is True:
                self.index(date_col)
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
                    self.df[f] = pd.to_datetime(self.df[f]).apply(convert)
                except ValueError:
                    pass
        except KeyError:
            self.warning("Can not find colums " + " ".join(fields))
            return
        except Exception as e:
            self.err(e, self.date, "Can not process date field")

    def dateindex(self, datafield, indexfield="date_index"):
        """
        Set a datetime index from a column
        """
        try:
            self.df = self._dateindex(datafield, indexfield)
        except Exception as e:
            self.err(e)

    def dateindex_(self, datafield, indexfield="date_index"):
        """
        Returns a DataSwim instance index from a column
        """
        try:
            df = self._dateindex(datafield, indexfield)
        except Exception as e:
            self.err(e)
            return
        return self.duplicate(df=df)

    def _dateindex(self, datafield, indexfield):
        """
        Returns a datetime index from a column
        """
        df = self.df.copy()
        try:
            df = df.set_index(pd.DatetimeIndex(df[datafield]))
        except Exception as e:
            msg = "Can not reindex with datafield " + \
                datafield + " and indexfield " + indexfield
            self.err(e, msg)
            return
        if self.autoprint is True:
            self.ok("Added a datetime index from column", datafield)
        return df

    def rangeindex(self, index_col="index"):
        """
        Index the main dataframe
        """
        try:
            self.df = self._rangeindex(index_col)
        except Exception as e:
            self.err(e)

    def rangeindex_(self, index_col="index"):
        """
        Returns an indexed DataSwim instance
        """
        try:
            return self.duplicate(self._rangeindex(index_col))
        except Exception as e:
            self.err(e)

    def _rangeindex(self, index_col):
        """
        Returns a range indexed dataframe
        """
        df = self.df
        try:
            df = df.reindex(index=range(len(df)))
            #vals = range(0, len(df[df[0]]))
            #index = pd.RangeIndex(vals)
            #df.index = index
        except Exception as e:
            msg = "Can not reindex"
            self.err(e, msg, self._rangeindex)
            return
        if self.autoprint is True:
            self.ok("Added a range index")
        return df

    def to_int(self, *fields):
        """
        Convert some columns values to integers
        """
        try:
            for el in fields:
                self.df[el] = self.df[el].apply(lambda x: int(x))
        except Exception as e:
            self.err(e)
    """
    def index_fill(self, dateindex=None, index_col=None, fill_col=None, quiet=False):
        ""
        Add a column from index and/or fill nans in a column
        ""
        try:
            self = self._index_fill(dateindex, index_col, fill_col, quiet)
        except Exception as e:
            self.err(e)

    def index_fill_(self, dateindex=None, index_col=None, fill_col=None, quiet=False):
        ""
        Returns a DataSwim instance with a column from index and/or fill nans in a column
        ""
        try:
            return self._index_fill(dateindex, index_col, fill_col, quiet)
        except Exception as e:
            self.err(e)

    def _index_fill(self, dateindex, index_col, fill_col, quiet):
        ""
        Add a column from index and/or fill nans in a column
        ""
        if dateindex is None and index_col is None and fill_col is None and quiet is False:
            if quiet is False:
                self.debug(
                    "Method index_fill: please provide at least one parameter")
            return
        ds2 = self.duplicate()
        if dateindex is not None:
            try:
                ds2 = ds2.dateindex_(dateindex)
            except Exception as e:
                self.err(e, self._index_fill, "Can not create date index")
                return
        if index_col is not None:
            try:
                ds2 = ds2.index_col_(index_col)
            except Exception as e:
                self.err(e, self._index_fill, "Can not create index col")
                return
        if fill_col is not None:
            try:
                ds2 = ds2.fill_nan_(0, fill_col)
            except Exception as e:
                self.err(e, self._index_fill, "Can not fill nans")
                return
        # if self.autoprint is True:
        #    self.ok("Indexed dataframe from column", dateindex)
        return ds2
    """
