# @PydevCodeAnalysisIgnore
import arrow
import numpy as np
import pandas as pd
from numpy.core.numeric import nan
from goerr.colors import colors
from ..errors import Error
from ..messages import Message


class Clean(Error, Message):
    """
    Class to clean the data
    """

    def drop_nan(self, col: str=None, method: str="all", **kwargs):
        """
        Drop rows with NaN values from the main dataframe

        :param col: name of the column, defaults to None. Drops in 
        :type col: str, optional
        :param method: ``how`` param for ``df.dropna``, defaults to "all"
        :type method: str, optional
        :param \*\*kwargs: params for ``df.dropna``
        :type \*\*kwargs: optional

        :example: ``ds.drop_nan("mycol")``
        """
        try:
            if col is None:
                self.df = self.df.dropna(how=method, **kwargs)
            else:
                self.df = self.df[self.df[col].notnull()]
        except Exception as e:
            self.err(e, "Error dropping nan values")

    def nan_empty(self, col: str):
        """
        Fill empty values with NaN values

        :param col: name of the colum
        :type col: str

        :example: ``ds.nan_empty("mycol")``
        """
        try:
            self.df[col] = self.df[col].replace('', nan)
            self.ok("Filled empty values with nan in column " + col)
        except Exception as e:
            self.err(e, "Can not fill empty values with nan")

    def zero_nan(self, *cols):
        """
        Converts zero values to nan values in selected columns

        :param \*cols: names of the colums
        :type \*cols: str, at least one

        :example: ``ds.zero_nan("mycol1", "mycol2")``
        """
        if len(cols) == 0:
            self.warning("Can not nan zero values if a column name "
                         "is not provided")
        df = self._zero_nan(*cols)
        if df is None:
            self.err("Can not fill zero values with nan")
            return
        self.df = df

    def _zero_nan(self, *cols):
        try:
            df = self.df.copy()
            for col in cols:
                if col not in df.columns:
                    self.warning("Column " + col + " does not exist")
                    return
                df = df.replace({col: {0: nan}})
            if len(cols) > 1:
                self.ok("Replaced 0 values by nan in columns",
                        str(cols))
            else:
                self.ok("Replaced 0 values by nan in column",
                        col)
            return df
        except Exception as e:
            self.err(e)

    def fill_nan(self, val: str, *cols):
        """
        Fill NaN values with new values in the main dataframe

        :param val: new value
        :type val: str
        :param \*cols: names of the colums
        :type \*cols: str, at least one

        :example: ``ds.fill_nan("new value", "mycol1", "mycol2")``
        """
        df = self._fill_nan(val, *cols)
        if df is not None:
            self.df = df
        else:
            self.err("Can not fill nan values")

    def _fill_nan(self, val, *cols):
        cols = list(cols)
        if len(cols) == 0:
            cols = self.df.columns.values
        df = None
        try:
            df = self.df.copy()
            for el in cols:
                try:
                    df[el] = df[[el]].fillna(val)
                except KeyError:
                    self.warning("Can not find column", el)
                    return
        except Exception as e:
            self.err(e, "Can not fill nan values")
            return
        self.ok("Filled nan values in columns", ",".join(cols))
        return df

    def fill_nulls(self, col: str):
        """
        Fill all null values with NaN values in a column.
        Null values are ``None`` or en empty string

        :param col: column name
        :type col: str

        :example: ``ds.fill_nulls("mycol")``
        """
        n = [None, ""]
        try:
            self.df[col] = self.df[col].replace(n, nan)
        except Exception as e:
            self.err(e)

    def to_int(self, *cols, **kwargs):
        """
        Convert some column values to integers

        :param \*cols: names of the colums
        :type \*cols: str, at least one
        :param \*\*kwargs: keyword arguments for ``pd.to_numeric``
        :type \*\*kwargs: optional

        :example: ``ds.to_int("mycol1", "mycol2", errors="coerce")``
        """
        try:
            for col in cols:
                self.df[col] = pd.to_numeric(self.df[col], **kwargs)
        except Exception as e:
            self.err(e, "Can not convert column values to integer")
            return
        self.ok("Converted column values to integers")

    def to_float(self, col: str, **kwargs):
        """
        Convert colums values to float

        :param col: name of the colum
        :type col: str, at least one
        :param \*\*kwargs: keyword arguments for ``df.astype``
        :type \*\*kwargs: optional

        :example: ``ds.to_float("mycol1")``
        """
        try:
            self.df[col] = self.df[col].astype(np.float64, **kwargs)
            self.ok("Converted column values to float")
        except Exception as e:
            self.err(e, "Error converting to float")

    def to_type(self, dtype: type, *cols, **kwargs):
        """
        Convert colums values to a given type in the 
        main dataframe

        :param dtype: a type to convert to: ex: ``str``
        :type dtype: type
        :param \*cols: names of the colums
        :type \*cols: str, at least one
        :param \*\*kwargs: keyword arguments for ``df.astype``
        :type \*\*kwargs: optional

        :example: ``ds.to_type(str, "mycol")``
        """
        try:
            allcols = self.df.columns.values
            for col in cols:
                if col not in allcols:
                    self.err("Column " + col + " not found")
                    return
                self.df[col] = self.df[col].astype(dtype, **kwargs)
        except Exception as e:
            self.err(e, "Can not convert to type")

    def fdate(self, *cols, precision: str="S", format: str=None):
        """
        Convert column values to formated date string

        :param \*cols: names of the colums
        :type \*cols: str, at least one
        :param precision: time precision: Y, M, D, H, Min S, defaults to "S"
        :type precision: str, optional
        :param format: python date format, defaults to None
        :type format: str, optional

        :example: ``ds.fdate("mycol1", "mycol2", precision)``
        """

        def formatdate(row):
            return row.strftime(format)

        def convert(row):
            encoded = '%Y-%m-%d %H:%M:%S'
            if precision == "Min":
                encoded = '%Y-%m-%d %H:%M'
            elif precision == "H":
                encoded = '%Y-%m-%d %H'
            elif precision == "D":
                encoded = '%Y-%m-%d'
            elif precision == "M":
                encoded = '%Y-%m'
            elif precision == "Y":
                encoded = '%Y'
            return row.strftime(encoded)

        try:
            for f in cols:
                try:
                    if format is None:
                        self.df[f] = pd.to_datetime(self.df[f]).apply(convert)
                    else:
                        self.df[f] = pd.to_datetime(
                            self.df[f]).apply(formatdate)
                except ValueError as e:
                    self.err(e, "Can not convert date")
                    return
        except KeyError:
            self.warning("Can not find colums " + " ".join(cols))
            return
        except Exception as e:
            self.err(e, "Can not process date col")

    def timestamps(self, col: str, **kwargs):
        """"
        Add a timestamps column from a date column

        :param col: name of the timestamps column to add
        :type col: str
        :param \*\*kwargs: keyword arguments for ``pd.to_datetime``
        :type \*\*kwargs: optional

        :example: ``ds.timestamps("mycol")``
        """
        try:
            name = "Timestamps"
            if "name" in kwargs:
                name = kwargs["name"]
            if "errors" not in kwargs:
                kwargs["errors"] = "coerce"
            if "unit" in kwargs:
                kwargs["unit"] = "ms"
            try:
                self.df[col] = pd.to_datetime(self.df[col], **kwargs)
            except TypeError:
                pass
            ts = []
            for el in self.df[col]:
                ts.append(arrow.get(el).timestamp)
            self.df[name] = ts
        except Exception as e:
            self.err(e, "Can not convert to timestamps")

    def date(self, col: str, **kwargs):
        """
        Convert a column to date type

        :param col: column name
        :type col: str
        :param \*\*kwargs: keyword arguments for ``pd.to_datetime`` 
        :type \*\*kwargs: optional

        :example: ``ds.date("mycol")``
        """
        try:
            self.df[col] = pd.to_datetime(self.df[col], **kwargs)
        except Exception as e:
            self.err(e, "Can not convert to date")

    def dateindex(self, col: str):
        """
        Set a datetime index from a column

        :param col: column name where to index the date from
        :type col: str

        :example: ``ds.dateindex("mycol")``
        """
        df = self._dateindex(col)
        if df is None:
            self.err("Can not create date index")
            return
        self.df = df
        self.ok("Added a datetime index from column", col)

    def _dateindex(self, col: str) -> pd.DataFrame:
        try:
            index = pd.DatetimeIndex(self.df[col])
            df = self.df.set_index(index)
            return df
        except Exception as e:
            self.err(e, "Can not index with column " +
                     colors.bold(col))

    def index(self, col: str):
        """
        Set an index to the main dataframe

        :param col: column name where to index from
        :type col: str

        :example: ``ds.index("mycol")``
        """
        df = self._index(col)
        if df is None:
            self.err("Can not create index")
            return
        self.df = df

    def _index(self, col: str) -> pd.DataFrame:
        try:
            df = self.df.set_index(self.df[col])
        except Exception as e:
            self.err(e, self._index, "Can not find column " +
                     colors.bold(col) + " in data")
            return
        self.ok("Added an index from column", col)
        return df

    def strip(self, col: str):
        """
        Remove leading and trailing white spaces in a column's values

        :param col: name of the column
        :type col: str

        :example: ``ds.strip("mycol")``
        """
        def remove_ws(row):
            val = str(row[col])
            if " " in val.startswith(" "):
                row[col] = val.strip()
            return row

        try:
            self.df.apply(remove_ws)
        except Exception as e:
            self.err(e, "Can not remove white space in column")
            return
        self.ok("White space removed in column values")

    def strip_cols(self):
        """
        Remove leading and trailing white spaces in columns names

        :example: ``ds.strip_cols()``
        """
        cols = {}
        skipped = []
        for col in self.df.columns.values:
            try:
                cols[col] = col.strip()
            except Exception:
                skipped.append(str(col))
        self.df = self.df.rename(columns=cols)
        self.ok("White spaces removed in columns names")
        if len(skipped) > 0:
            self.info("Skipped columns", ','.join(
                skipped), "while removing white spaces")

    def roundvals(self, col: str, precision: int=2):
        """
        Round floats in a column. Numbers are going to be
        converted to floats if they are not already

        :param col: column name
        :type col: str
        :param precision: float precision, defaults to 2
        :param precision: int, optional

        :example: ``ds.roundvals("mycol")``
        """
        try:
            self.df[col] = self.df[col].astype("float64")
            self.df[col] = self.df[col].apply(lambda x: round(x, precision))
        except Exception as e:
            self.err(e, "Can not round column values")
            return
        self.ok("Rounded values in column " + col)

    def replace(self, col: str, searchval: str, replaceval: str):
        """
        Replace a value in a column in the main dataframe

        :param col: column name
        :type col: str
        :param searchval: value to replace
        :type searchval: str
        :param replaceval: new value
        :type replaceval: str

        :example: ``ds.replace("mycol", "value", "new_value")``
        """
        try:
            self.df[col] = self.df[col].replace(searchval, replaceval)
        except Exception as e:
            self.err(e, "Can not replace value in column")

    def creplace(self, col: str, searchval: str, replaceval: str):
        """
        Replace a value in a column in the main dataframe
        if the value is contained

        :param col: column name
        :type col: str
        :param searchval: value to replace
        :type searchval: str
        :param replaceval: new value
        :type replaceval: str

        :example: ``ds.creplace("mycol", "value", "new_value")``
        """
        try:
            self.df[col] = self.df[col].str.replace(searchval,
                                                    replaceval)
        except Exception as e:
            self.err("Can not replace value in column")

    def format_date_(self, date):
        """
        Formats a date
        """
        return date.strftime('%Y-%m-%d %H:%M:%S')
