# @PydevCodeAnalysisIgnore
from datetime import datetime
import arrow
import pandas as pd
import numpy as np


class Select():
    """
    Class to select data
    """

    def first_(self):
        """
        Select the first row
        """
        try:
            val = self.df.iloc[0]
            return val
        except Exception as e:
            self.err(e, "Can not select first row")

    def limit(self, r=5):
        """
        Limit selection to a range in the main dataframe
        """
        try:
            self.df = self.df[:r]
        except Exception as e:
            self.err(e, "Can not limit data")

    def limit_(self, r=5):
        """
        Returns a DataSwim instance with limited selection
        """
        try:
            return self._duplicate_(self.df[:r])
        except Exception as e:
            self.err(e, "Can not limit data")

    def unique_(self, col):
        """
        Returns unique values in a column
        """
        try:
            df = self.df.drop_duplicates(subset=[col], inplace=False)
            return list(df[col])
        except Exception as e:
            self.err(e, "Can not select unique data")

    def wunique_(self, col):
        """
        Weight unique values: returns a dataframe with a count
        of unique values
        """
        try:
            s = pd.value_counts(self.df[col].values)
            df = pd.DataFrame(s, columns=["Number"])
            return df
        except Exception as e:
            self.err(e, "Can not weight unique data")

    def vrange(self, **args):
        """
        Limit the data in a time range from a date offset
        """
        df = self._range(**args)
        if df is None:
            self.err("Can not select range data")
            return
        self.df = df

    def range_(self, **args):
        """
        Limit the data in a time range from a date offset
        """
        df = self._range(**args)
        if df is None:
            self.err("Can not select range data")
            return
        return self._duplicate_(df)

    def _range(self, **args):
        try:
            df = self.df[:self.df.first_valid_index() + pd.DateOffset(**args)]
            return df
        except Exception as e:
            self.err(e, "Can not select range data")
            return

    def nowrange(self, col, timeframe):
        """
        Set the main dataframe with rows within a date range from now
        ex: ds.nowrange("Date", "3D") for a 3 days range. Units are: S,
        H, D, W, M, Y
        """
        df = self._nowrange(col, timeframe)
        if df is None:
            self.err("Can not select range data from now")
            return
        self.df = df

    def nowrange_(self, col, timeframe):
        """
        Returns a Dataswim instance with rows within a date range from now
        ex: ds.nowrange("Date", "3D") for a 3 days range. Units are: S,
        H, D, W, M, Y
        """
        df = self._nowrange(col, timeframe)
        if df is None:
            self.err("Can not select range data from now")
            return
        return self._duplicate_(df)

    def _nowrange(self, col, timeframe):
        try:
            # df = self.df[self.df[col].dt.date < datetime.now().date(
            # ) + pd.to_timedelta(interval, unit=unit)]
            unit = timeframe[-1:]
            i = int(timeframe[0:(len(timeframe) - 1)])
            interval = int(np.negative(i))
            if unit == "S":
                date = arrow.now().shift(seconds=interval).naive
            elif unit == "m":
                date = arrow.now().shift(minutes=interval).naive
            elif unit == "H":
                date = arrow.now().shift(hours=interval).naive
            elif unit == "D":
                date = arrow.now().shift(days=interval).naive
            elif unit == "W":
                date = arrow.now().shift(weeks=interval).naive
            elif unit == "M":
                date = arrow.now().shift(months=interval).naive
            elif unit == "Y":
                date = arrow.now().shift(years=interval).naive
            else:
                self.err("Wrong unit " + unit)
                return
            df = self.df.copy()
            df = df[df[col] > date]
            return df
        except Exception as e:
            self.err(e, "Can not select range data from now")

    def daterange(self, datecol, date_start, op, **args):
        """
        Returns rows in a date range
        """
        df = self._daterange(datecol, date_start, op, **args)
        if df is None:
            self.err("Can not select date range data")
        self.df = df

    def daterange_(self, datecol, date_start, op, **args):
        """
        Returns a DataSwim instance with rows in a date range
        """
        df = self._daterange(datecol, date_start, op, **args)
        if df is None:
            self.err("Can not select date range data")
        return self._duplicate_(df)

    def _daterange(self, datecol, date_start, op, **args):
        try:
            idate = pd.Timestamp(date_start)
            self.df[datecol] = pd.to_datetime(self.df[datecol])
            if op == "+":
                end_date = idate + pd.DateOffset(**args)
                start_date = idate
            elif op == "-":
                start_date = idate - pd.DateOffset(**args)
                end_date = idate
            mask = (self.df[datecol] >= start_date) & (
                self.df[datecol] <= end_date)
            df = self.df.loc[mask]
            return df
        except Exception as e:
            self.err(e, self._daterange, "Can not select date range data")

    def subset(self, *args):
        """
        Set the main dataframe to a subset based in positions
        Select a subset of the main dataframe based on position:
        ex: ds.subset(0,10) or ds.subset(10) is equivalent: it starts
        at the first row if only one argument is provided
        """
        df = self._subset(*args)
        if df is None:
            self.err("Can get subset of data")
            return
        self.df = df

    def subset_(self, *args):
        """
        Returns a Dataswim instance with a subset data based in positions
        Select a subset of the main dataframe based on position:
        ex: ds.subset(0,10) or ds.subset(10) is equivalent: it starts
        at the first row if only one argument is provided
        """
        df = self._subset(*args)
        if df is None:
            self.err("Can not get subset of data")
            return
        return self._duplicate_(df)

    def _subset(self, *args):
        try:
            start = 0
            end = args[0]
            if len(args) > 1:
                start = args[0]
                end = args[1]
            return self.df.iloc[start: end]
        except Exception as e:
            self.err(e, "Can not select data")
