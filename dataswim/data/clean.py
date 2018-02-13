# -*- coding: utf-8 -*-
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
        Returns a DataSwim instance with zero values to nan values in
        selected columns
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

    def replace(self, col, searchval, replaceval):
        """
        Replace a value in a column in the main dataframe
        """
        try:
            self.df = self._replace(col, searchval, replaceval)
        except Exception as e:
            self.err(e, self.replace, "Can not replace value in column")

    def replace_(self, col, searchval, replaceval):
        """
        Returns a Dataswim instance with replaced values in a column
        """
        try:
            return self._replace(col, searchval, replaceval)
        except Exception as e:
            self.err(e, self.replace_, "Can not replace value in column")

    def _replace(self, col, searchval, replaceval):
        """
        Replace a value in a colum
        """
        df = self.df.copy()
        try:
            df[col] = df[col].replace(searchval, replaceval)
            return df
        except Exception as e:
            self.err(e, self._replace, "Can not replace value in column")

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

        def convert(val):
            try:
                return int(val)
            except Exception as e:
                print(val, str(type(val)))
                raise(e)
                return val
        try:
            ds2.df[field] = ds2.df[field].apply(convert)
            self.df = ds2.df
        except Exception as e:
            self.err(e, self.to_int,
                     "Can not convert column values to integer")
            return
        if self.autoprint is True:
            self.ok("Converted column values to integers")

    def to_float(self, *cols):
        """
        Convert colums values to float
        """
        try:
            df = self.to_type("float64", *cols)
            self.df = df
        except Exception as e:
            self.err(e, self.to_type, "Can not convert column values to float")
            return
        if self.autoprint is True:
            self.ok("Converted column values to float")

    def to_type(self, dtype, *cols):
        """
        Convert colums values to a given type
        """
        df = self.df.copy()
        allcols = df.columns.values
        try:
            for col in cols:
                if col not in allcols:
                    self.err(self.to_type, "Column " + col + " not found")
                    return
                df[col] = df[col].astype(dtype)
            return df
        except Exception as e:
            self.err(e)

    def timestamps(self, col, **kwargs):
        """
        Add a timestamps column from a date column
        """
        try:
            name = "Timestamps"
            if "name" in kwargs:
                name = kwargs["name"]
            if "errors" not in kwargs:
                kwargs["errors"] = "coerce"
            if "unit" in kwargs:
                kwargs["unit"] = "ms"
            #self.add(name, 0)
            try:
                self.df[col] = pd.to_datetime(self.df[col], **kwargs)
            except TypeError:
                pass
            ts = []
            for el in self.df[col]:
                ts.append(arrow.get(el).timestamp)
            self.df[name] = ts
        except Exception as e:
            self.err(e, self.timestamps, "Can not convert to timestamps")

    def date(self, *fields, precision="S"):
        """
        Convert column values to properly formated datetime
        """
        def convert(row):
            try:
                t1 = row.timetuple()
                int(time.mktime(t1))
            except Exception:
                return nan
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

    def index(self, indexcol):
        """
        Set an index to the main dataframe
        """
        try:
            self.df = self._index(indexcol)
        except KeyError as e:
            self.err(e, self.index, "Can not create index")

    def index_(self, indexcol):
        """
        Returns a Dataswim instance with an index
        """
        try:
            return self._index(indexcol)
        except KeyError as e:
            self.err(e, self.index_, "Can not create index")

    def _index(self, indexcol):
        """
        Set an index to the main dataframe
        """
        df = self.df.copy()
        try:
            df = df.set_index(df[indexcol])
        except KeyError as e:
            self.err(e, self._index, "Can not find column " +
                     colors.bold(indexcol) + " in data")
            return
        except Exception as e:
            msg = "Can not index with columns " + \
                colors.bold(indexcol) + " and indexfield "
            self.err(e, self._index, msg)
            return
        if self.autoprint is True:
            self.ok("Added an index from column", indexcol)
        return df

    def strip(self, col):
        """
        Remove white space in a column's values
        """
        def remove_ws(row):
            val = str(row[col])
            if " " in val:
                row[col] = val.replace(" ", "")
            return row

        try:
            self.apply(remove_ws)
        except Exception as e:
            self.err(e, self.strip, "Can not remove white space in column")
            return
        if self.autoprint is True:
            self.ok("White space removed in column values")

    def strip_cols(self):
        """
        Remove white space in columns names
        """
        try:
            cols = {}
            skipped = []
            for col in self.df.columns.values:
                try:
                    cols[col] = col.strip()
                except Exception:
                    skipped.append(str(col))
            self.df = self.df.rename(columns=cols)
        except Exception as e:
            self.err(
                e,
                self.strip_cols,
                "Can not strip white space in columns")
            return
        if self.autoprint is True:
            self.ok("White space removed in columns names")
            if len(skipped) > 0:
                self.info("Skipped columns", ','.join(
                    skipped), "while removing white space")

    def round(self, col, precision=2):
        """
        Round floats in a column
        """
        try:
            self.to_float([col])
            self.df[col] = self.df[col].apply(lambda x: round(x, precision))
        except Exception as e:
            self.err(e, self.round, "Can not round column values")
            return
        if self.autoprint is True:
            self.ok("Rounded values in column " + col)

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
            self.set(self._trimquants(col, inf, sup))
        except Exception as e:
            self.err(e, self.trimquants, "Can not trim quantiles")

    def trimsquants(self, col, sup):
        """
        Remove superior quantiles from the dataframe
        """
        try:
            self.set(self._trimquants(col, None, sup))
        except Exception as e:
            self.err(e, self.trimsquants, "Can not trim superior quantiles")

    def trimiquants(self, col, inf):
        """
        Remove superior and inferior quantiles from the dataframe
        """
        try:
            self.set(self._trimquants(col, inf, None))
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

    def format_date_(self, date):
        """
        Formats a date
        """
        return date.strftime('%Y-%m-%d %H:%M:%S')

    def transform_(self, dateindex=None, index_col=None,
                   fill_col=None, num_col=None, df=None):
        """
        Returns a DataSwim instance transformed according to the
        given parameters
        """
        if df is None:
            if self.df is None:
                self.err(self._transform,
                         "No dataframe: please provide one "
                         "in parameters or set it")
                return
            df = self.df.copy()
        ds2 = self.clone_(df)
        if dateindex is None and index_col is None and fill_col \
                is None and num_col is None:
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
