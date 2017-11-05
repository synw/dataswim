# -*- coding: utf-8 -*-

import dataset
import holoviews as hv
import pandas as pd
import pandas_profiling
from goerr import err


class Plot():

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df
        self.x_field = None
        self.y_field = None
        self.chart_opts = dict(width=940)
        self.chart_style = dict(color="blue")

    def chart(self, x_field, y_field, chart_type="line"):
        """
        Initialize chart options
        """
        self.x_field = x_field
        self.y_field = y_field
        chart = self._get_chart(chart_type, x_field, y_field)
        if err.exists:
            err.throw()
        return chart

    def bar(self):
        """
        Get a bar chart
        """
        return self._get_chart("bar")

    def line(self):
        """
        Get a line chart
        """
        return self._get_chart("line")

    def point(self):
        """
        Get a point chart
        """
        return self._get_chart("point")

    def line_point(self, colors={"line": "yellow", "point": "navy"}):
        """
        Get a line and point chart
        """
        style = self.chart_style
        style["color"] = colors["line"]
        l = self._get_chart("line", style=style)
        style["color"] = colors["point"]
        p = self._get_chart("point", style=style)
        return l * p

    def color(self, color):
        """
        Set chart color
        """
        self.chart_style["color"] = color

    def width(self, width):
        """
        Set chart width
        """
        self.chart_opts["width"] = width

    def height(self, height):
        """
        Set chart height
        """
        self.chart_opts["height"] = height

    def _get_chart(self, chart_type="line", x_field=None, y_field=None, style=None):
        """
        Get a full chart object
        """
        if x_field is None:
            x_field = self.x_field
        if y_field is None:
            y_field = self.y_field
        if style is None:
            style = self.chart_style
        base_chart = self._get_base_chart(
            x_field, y_field, chart_type)
        chart = base_chart(plot=self.chart_opts, style=style)
        return chart

    def _get_base_chart(self, x_field, y_field, chart_type="line"):
        """
        Get a base chart object
        """
        chart = None
        if chart_type == "line":
            chart = hv.Curve(self.df, kdims=[x_field], vdims=[y_field])
        elif chart_type == "point":
            chart = hv.Scatter(self.df, kdims=[x_field], vdims=[y_field])
        elif chart_type == "bar":
            chart = hv.Bars(self.df, kdims=[x_field], vdims=[y_field])
        if chart is None:
            err.new("Chart type " + chart_type + " unknown")
        return chart


class Df():
    """
    Class for manipulating dataframes
    """

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df
        self.backup_df = df

    def set(self, df):
        """
        Set a main dataframe
        """
        df2 = df.copy()
        self.df = df2

    def backup(self):
        """
        Backup the main dataframe
        """
        self.backup_df = self.df

    def restore(self):
        """
        Restore the main dataframe
        """
        self.df = self.backup_df

    def load_csv(self, url):
        """
        Initialize the main dataframe from csv data
        """
        self.df = pd.read_csv(url)

    def reduce(self, fields):
        """
        Limit a dataframe to some columns
        """
        return self.df[fields]

    def to_int(self, fieldname):
        """
        Convert a column values to integers
        """
        self.df[fieldname] = self.df[fieldname].apply(lambda x: int(x))

    def date(self, fields):
        """
        Convert column values to datetime from either a list 
        of column names or a single column name string
        """
        if type(fields) == str:
            self.df[fields] = pd.to_datetime(self.df[fields]).apply(
                lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            for f in fields:
                self.df[f] = pd.to_datetime(self.df[f]).apply(
                    lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

    def index(self, datafield, indexfield):
        """
        Set a datetime index from a column
        """
        f = {indexfield: self.df[datafield]}
        self.df = self.df.assign(**f)
        self.df = self.df.set_index(indexfield)
        self.df.index = pd.to_datetime(self.df.index)

    def contains(self, value, field):
        """
        Set the main dataframe to rows that contains a string value in a column
        """
        self.df = self.df[self.df[field].str.contains(value) == True]

    def exact(self, value, field):
        """
        Set the main dataframe to rows that has the exact string value in a column
        """
        self.df = self.df[self.df[field].isin([value])]

    def concat(self, dfs):
        """
        Concatenate dataframes from a list and set it to the main dataframe
        """
        self.df = pd.concat(dfs)

    def add(self, field, value):
        """
        Add a columns with default values
        """
        self.df[field] = value

    def date_field(self, field):
        """
        Add a date column from the datetime index
        """
        self.df[field] = self.df.index.values

    def resample(self, time_unit="1Min"):
        """
        Resample the main dataframe to a time period
        """
        df = self.df.resample(time_unit)
        return df

    def range(self, num, unit):
        """
        Limit the data in a time range
        """
        self.df = self.df[self.df.last_valid_index() -
                          pd.DateOffset(num, unit):]

    def head(self):
        """
        Print the main dataframe's head in notebook
        """
        return self.df.head()

    def look(self, df=None, p=True):
        """
        Print basic data info in notebook
        """
        if df is None:
            df = self.df
        num = len(self.df.index)
        if p is True:
            print(num, "rows")
            print("Fields:", ", ".join(list(self.df)))
        else:
            return p

    def describe(self):
        """
        Print a description of the data in notebook
        """
        self.look()
        return self.df.describe()

    def report(self, df=None):
        """
        Returns a dataframe profiling report to print in notebooks
        """
        if df is None:
            df = self.df
        return pandas_profiling.ProfileReport(df)

    def display(self, fields):
        """
        Display some columns head in notebook
        """
        if type(fields) == str:
            df2 = self.df[[fields]]
        else:
            df2 = self.df[fields]
        return df2.head()

    def drop(self):
        """
        Drop NaN values from the main dataframe
        """
        self.df = self.df.dropna()

    def fill(self, fieldname, val=0):
        """
        Fill NaN values with new values
        """
        self.df[fieldname] = self.df[fieldname].fillna(val)

    def nulls(self, fieldname, val=0):
        """
        Fill null values with new values
        """
        nvals = ["None", "NaN", "Null", "none", "null"]

        def isnull(x):
            global nulls
            if type(x) == str:
                if x in nvals:
                    return val
                else:
                    return x

        self.df[fieldname] = self.df[fieldname].apply(isnull)

    def count(self):
        """
        Count the number of rows of the main dataframe
        """
        total = len(self.df.index)
        return total


class Db():
    """
    Class for manipulating databases
    """

    def __init__(self, db=None):
        """
        Initialize with an empty db
        """
        self.db = db

    def connect(self, url):
        """
        Connect to the database and set it as main database
        """
        self.db = dataset.connect(url)

    def load(self, table):
        """
        Set the main dataframe from a table's data
        """
        self.df = self.getall(table)

    def tables(self, name=None, p=True):
        """
        Print existing tables in a database
        """
        t = self.db.tables
        if name is not None:
            pmodels = [x for x in t if name in x]
        else:
            pmodels = t
        if p is True:
            print(pmodels)
        return pmodels

    def count_rows(self, name, p=True):
        """
        Count rows for a table
        """
        data = {}
        for m in self.tables(name, False):
            num = self.db[m].count()
            data[m] = num
            if p is True and num > 0:
                print(m, num)
        print("[end]")
        return data

    def getall(self, table):
        """
        Get all rows values for a table
        """
        res = self.db[table].all()
        df = pd.DataFrame(list(res))
        return df

    def show(self, table=None, p=True):
        """
        Display info about a table
        """
        if table is None:
            df = self.df
        else:
            df = self.getall(table)
        num = len(self.df.index)
        if p is True:
            print(num, "rows")
            print("Fields:", ", ".join(list(df)))
        return ds.head()


class DataSwim(Plot, Db, Df):
    """
    Main class
    """
    pass


ds = DataSwim()
