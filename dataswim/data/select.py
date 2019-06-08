# @PydevCodeAnalysisIgnore
import arrow
import pandas as pd
import numpy as np
from ..errors import Error


class Select(Error):
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

    """def ranged(self, end_date, start_date=None):
        ""
        Limit the data in a time range between two dates. The
        dataframe must have a valid date index
        ""
        try:
            if start_date is None:
                start_date = self.df.index.get_values()[0]
            self.df = self.df.loc[start_date: end_date]
        except Exception as e:
            self.err("Can not select range data", e)

    def rangeo(self, **kwargs):
        ""
        Limit the data in a time range between an end date and an offset.
        The dataframe must have a valid date index. The offset must be
        provided: ex: months=3. An end_date can be provided optionally. If
        not provided the last index of the dataframe will be used as end date
        ""
        try:
            if "end_date" not in kwargs:
                end_date = self.df.index.get_values()[len(self.df.index)-1]
            else:
                end_date = kwargs["end_date"]
            if "years" in kwargs:
                start_date = end_date - pd.DateOffset(years=kwargs["years"])
            if "months" in kwargs:
                print("M", kwargs["months"])
                start_date = end_date - pd.DateOffset(months=kwargs["months"])
            if "days" in kwargs:
                start_date = end_date - pd.DateOffset(days=kwargs["days"])
            if "hours" in kwargs:
                start_date = end_date - pd.DateOffset(hours=kwargs["hours"])
            if "minutes" in kwargs:
                start_date = end_date - \
                    pd.DateOffset(minutes=kwargs["minutes"])
            if "seconds" in kwargs:
                start_date = end_date - \
                    pd.DateOffset(seconds=kwargs["seconds"])
            self.df = self.df.loc[start_date: end_date]
        except Exception as e:
            self.err("Can not select range data", e)"""

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
                date = arrow.utcnow().shift(seconds=interval)
            elif unit == "m":
                date = arrow.utcnow().shift(minutes=interval)
            elif unit == "H":
                date = arrow.utcnow().shift(hours=interval)
            elif unit == "D":
                date = arrow.utcnow().shift(days=interval)
            elif unit == "W":
                date = arrow.utcnow().shift(weeks=interval)
            elif unit == "M":
                date = arrow.utcnow().shift(months=interval)
            elif unit == "Y":
                date = arrow.utcnow().shift(years=interval)
            else:
                self.err("Wrong unit " + unit)
                return
            df = self.df.copy()
            df = df[df[col] > date.datetime]
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
