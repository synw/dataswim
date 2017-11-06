# -*- coding: utf-8 -*-

import holoviews as hv
from goerr import err


class Plot():

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df
        self.x_field = None
        self.y_field = None
        self.chart_opts = dict(width=940, show_legend=True)
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

    def point(self, df=None):
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
            chart = hv.Curve(self.df, kdims=[x_field], vdims=[
                             y_field], label="Test")
        elif chart_type == "point":
            chart = hv.Scatter(self.df, kdims=[x_field], vdims=[y_field])
        elif chart_type == "bar":
            chart = hv.Bars(self.df, kdims=[x_field], vdims=[y_field])
        if chart is None:
            err.new("Chart type " + chart_type + " unknown")
        return chart
