# @PydevCodeAnalysisIgnore
import time
import arrow
import pandas as pd
from numpy.core.numeric import nan
from goerr.colors import colors


class Clean():
    """
    Class to clean the data
    """

    def drop_nan(self, field=None, method="all", **kwargs):
        """
        Drop NaN values from the main dataframe
        """
        try:
            if field is None:
                self.df = self.df.dropna(how=method, **kwargs)
            else:
                self.df = self.df[self.df[field].notnull()]
        except Exception as e:
            self.error(e, "Error dropping nan values")

    def nan_empty(self, field):
        """
        Fill empty values with NaN values
        """
        try:
            self.df[field] = self.df[field].replace('', nan)
            self.ok("Filled empty values with nan in column " + field)
        except Exception as e:
            self.err(e, "Can not fill empty values with nan")

    def zero_nan(self, *fields):
        """
        Converts zero values to nan values in selected columns
        """
        df = self._zero_nan(*fields)
        if df is None:
            self.err("Can not fill zero values with nan")
            return
        self.df = df

    def zero_nan_(self, *fields):
        """
        Returns a DataSwim instance with zero values to nan values in
        selected columns
        """
        df = self._zero_nan(*fields)
        if df is None:
            self.err("Can not fill zero values with nan")
            return
        ds2 = self.clone_(quiet=True)
        ds2.df = df
        return ds2

    def _zero_nan(self, *fields):
        try:
            df = self.df.copy()
            for field in fields:
                if field not in df.columns:
                    self.warning("Column " + field + " does not exist")
                    return
                df = df.replace({field: {0: nan}})
            if len(fields) > 1:
                self.ok("Replaced 0 values by nan in columns",
                        str(fields))
            else:
                self.ok("Replaced 0 values by nan in column",
                        field)
            return df
        except Exception as e:
            self.err(e)

    def fill_nan(self, val, *fields):
        """
        Fill NaN values with new values in the main dataframe
        """
        df = self._fill_nan(val, *fields)
        if df is not None:
            self.df = df
        else:
            self.err("Can not fill nan values")

    def fill_nan_(self, val, *fields):
        """
        Returns a DataSwim instance with NaN values filled
        """
        df = self._fill_nan(val, *fields)
        if df is not None:
            return self._duplicate_(df=df)
        else:
            self.err("Can not fill nan values")

    def _fill_nan(self, val, *fields):
        fields = list(fields)
        if len(fields) == 0:
            fields = self.df.columns.values
        df = None
        try:
            df = self.df.copy()
            for el in fields:
                try:
                    df[el] = df[[el]].fillna(val)
                except KeyError:
                    self.warning("Can not find column", el)
                    return
        except Exception as e:
            self.err(e, "Can not fill nan values")
            return
        self.ok("Filled nan values in columns", ",".join(fields))
        return df

    def replace(self, col, searchval, replaceval):
        """
        Replace a value in a column in the main dataframe
        """
        df = self._replace(col, searchval, replaceval)
        if df is not None:
            self.df = df
        else:
            self.err("Can not replace value in column")

    def replace_(self, col, searchval, replaceval):
        """
        Returns a Dataswim instance with replaced values in a column
        """
        df = self._replace(col, searchval, replaceval)
        if df is not None:
            return self._duplicate_(df)
        else:
            self.err("Can not replace value in column")

    def _replace(self, col, searchval, replaceval):
        try:
            df = self.df.copy()
            df[col] = df[col].replace(searchval, replaceval)
            return df
        except Exception as e:
            self.err(e, "Can not replace value in column")

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

        def convert(val):
            return int(val)

        try:
            self.df[field] = self.df[field].apply(convert)
        except Exception as e:
            self.err(e, "Can not convert column values to integer")
            return
        self.ok("Converted column values to integers")

    def to_float(self, *cols):
        """
        Convert colums values to float
        """
        df = self.to_type("float64", *cols)
        if df is not None:
            self.df = df
        else:
            self.err("Can not convert column values to float")
            return
        self.ok("Converted column values to float")

    def to_type(self, dtype, *cols):
        """
        Convert colums values to a given type
        """
        try:
            df = self.df.copy()
            allcols = df.columns.values
            for col in cols:
                if col not in allcols:
                    self.err("Column " + col + " not found")
                    return
                df[col] = df[col].astype(dtype)
            return df
        except Exception as e:
            self.err(e, "Can not convert to type")

    def timestamps(self, col, **kwargs):
        """
        Add  a timestamps column from a date column
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

    def date(self, *fields, precision="S", format=None):
        """
        Convert column values to properly formated datetime
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
            for f in fields:
                try:
                    if format is None:
                        self.df[f] = pd.to_datetime(
                            pd.to_datetime(self.df[f]).apply(convert)
                            )
                    else:
                        self.df[f] = pd.to_datetime(
                            pd.to_datetime(self.df[f]).apply(formatdate)
                            )
                except ValueError as e:
                    self.err(e, "Can not convert date")
                    return
        except KeyError:
            self.warning("Can not find colums " + " ".join(fields))
            return
        except Exception as e:
            self.err(e, "Can not process date field")

    def dateindex(self, datafield):
        """
        Set a datetime index from a column
        """
        df = self._dateindex(datafield)
        if df is None:
            self.err("Can not index data")
            return
        self.df = df

    def dateindex_(self, datafield):
        """
        Returns a DataSwim instance index from a column
        """
        df = self._dateindex(datafield)
        if df is None:
            self.err("Can not index data")
            return
        return self._duplicate_(df)

    def _dateindex(self, datafield):
        try:
            index = pd.DatetimeIndex(self.df[datafield])
            df = self.df.set_index(index)
        except Exception as e:
            self.err(e, "Can not index with column " + 
                     colors.bold(datafield))
            return
        self.ok("Added a datetime index from column", datafield)
        return df

    def index(self, indexcol):
        """
        Set an index to the main dataframe
        """
        df = self._index(indexcol)
        if df is None:
            self.err("Can not create index")
            return
        self.df = df

    def index_(self, indexcol):
        """
        Returns a Dataswim instance with an index
        """
        df = self._index(indexcol)
        if df is None:
            self.err("Can not create index")
            return
        return self._duplicate_(df)

    def _index(self, indexcol):
        try:
            df = self.df.set_index(self.df[indexcol])
        except Exception as e:
            self.err(e, self._index, "Can not find column " + 
                     colors.bold(indexcol) + " in data")
            return
        self.ok("Added an index from column", indexcol)
        return df

    def strip(self, col):
        """
        Remove leading and trailing white spaces in a column's values
        """

        def remove_ws(row):
            val = str(row[col])
            if " " in val:
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

    def roundvals(self, col, precision=2):
        """
        Round floats in a column
        """
        try:
            self.df[col] = self.df[col].astype("float64")
            self.df[col] = self.df[col].apply(lambda x: round(x, precision))
        except Exception as e:
            self.err(e, "Can not round column values")
            return
        self.ok("Rounded values in column " + col)

    def format_date_(self, date):
        """
        Formats a date
        """
        return date.strftime('%Y-%m-%d %H:%M:%S')
