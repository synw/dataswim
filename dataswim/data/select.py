from datetime import datetime
import pandas as pd


class Select():
    """
    Class to select data
    """

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df

    def first_(self):
        """
        Returns the first row
        """
        return self._first()

    def _first(self):
        """
        Select the first row
        """
        try:
            val = self.df.iloc[0]
            return val
        except Exception as e:
            self.err(e, self.first, "Can not select first row")

    def limit(self, r=5):
        """
        Limit selection to a range in the main dataframe
        """
        try:
            self.df = self.df[:r]
        except Exception as e:
            self.err(e, self.limit, "Can not limit data")

    def limit_(self, r=5):
        """
        Returns a DataSwim instance with limited selection
        """
        try:
            return self.new(self.df[:r])
        except Exception as e:
            self.err(e)

    def unique_(self, column):
        """
        Returns unique values in a column
        """
        try:
            df = self.df.copy()
            df.drop_duplicates(subset=[column], inplace=True)
            return self.clone_(df)
        except Exception as e:
            self.err(e, self.unique_, "Can not select unique data")

    def range(self, **args):
        """
        Limit the data in a time range
        """
        try:
            self.df = self._range(**args)
        except Exception as e:
            self.err(e, self.range, "Can not select range data")
            return

    def _range(self, **args):
        """
        Limit the data in a time range
        """
        try:
            df = self.df[self.df.last_valid_index() -
                         pd.DateOffset(**args):]
            return df
        except Exception as e:
            self.err(e, self._range, "Can not select range data")
            return

    def range_(self, **args):
        """
        Limit the data in a time range
        """
        try:
            ds2 = self.clone_(self._range(**args))
            return ds2
        except Exception as e:
            self.err(e, self.range_, "Can not select range data")

    def nowrange(self, col, interval, unit="D"):
        """
        Set the main dataframe with rows within a date range from now
        """
        try:
            df = self._nowrange(col, interval, unit)
            self.set(df)
        except Exception as e:
            self.err(e, self.nowrange_, "Can not select range data from now")

    def nowrange_(self, col, interval, unit="D"):
        """
        Returns a Dataswim instance with rows within a date range from now
        """
        try:
            df = self._nowrange(col, interval, unit)
            return self.clone_(df)
        except Exception as e:
            self.err(e, self.nowrange_, "Can not select range data from now")

    def _nowrange(self, col, interval, unit):
        """
        Returns a dataframe with rows within a date range from now
        """
        try:
            df = self.df.copy()
            df = df[df[col].dt.date > datetime.now().date(
            ) - pd.to_timedelta(interval, unit=unit)]
            return df
        except Exception as e:
            self.err(e, self._nowrange, "Can not select range data from now")

    def daterange(self, datecol, date_start, op, **args):
        """
        Returns rows in a date range
        """
        try:
            self.df = self._daterange(datecol, date_start, op, **args)
        except Exception as e:
            self.err(e, self.daterange, "Can not select date range data")

    def daterange_(self, datecol, date_start, op, **args):
        """
        Returns a DataSwim instance with rows in a date range
        """
        try:
            df = self._daterange(datecol, date_start, op, **args)
            return self.clone_(df)
        except Exception as e:
            self.err(e, self.daterange_, "Can not select date range data")

    def _daterange(self, datecol, date_start, op, **args):
        """
        Returns rows in a date range
        """
        try:
            start_date = pd.Timestamp(date_start)
            self.df[datecol] = pd.to_datetime(self.df[datecol])
            if op == "+":
                end_date = start_date + pd.DateOffset(**args)
            elif op == "-":
                end_date = start_date - pd.DateOffset(**args)
            mask = (self.df[datecol] >= start_date) & (
                self.df[datecol] <= end_date)
            df = self.df.loc[mask]
            return df
        except Exception as e:
            self.err(e, self._daterange, "Can not select date range data")

    def to_records_(self):
        """
        Returns a list of dictionary records from the main dataframe
        """
        try:
            dic = self.df.to_dict(orient="records")
            return dic
        except Exception as e:
            self.err(e, self.to_records_, "Can not create records")

    def subset(self, *args):
        """
        Set the main dataframe to a subset based in positions
        """
        try:
            self.df = self._subset(*args)
        except Exception as e:
            self.err(e, self.subset, "Can get subset of data")

    def subset_(self, *args):
        """
        Returns a Dataswim instance with a subset data based in positions
        """
        try:
            df = self._subset(*args)
            return self.clone_(df)
        except Exception as e:
            self.err(e, self.subset_, "Can not get subset of data")

    def _subset(self, *args):
        """
        Select a subset of the main dataframe based on position:
        ex: ds.subset(0,10) or ds.subset(10) is equivalent: it starts
        at the first row if only one argument is provided
        """
        try:
            end = args[0]
            if len(args) > 1:
                start = args[0]
                end = args[1]
            return self.df.iloc[start: end]
        except Exception as e:
            self.err(e, self._subset, "Can not select data")

    def nulls_(self, field):
        """
        Return all null rows
        """
        try:
            null_rows = self.df[field][self.df[field].isnull()]
        except Exception as e:
            self.err(e, self.nulls_, "Can not select null rows")
        return null_rows
