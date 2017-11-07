# -*- coding: utf-8 -*-

import holoviews as hv
from goerr import err


X = None
Y = None


class Plot():

    def chart(self, x_field=None, y_field=None, chart_type="line", opts=None, style=None, label=None):
        """
        Initialize chart options
        """
        global X, Y
        if x_field is None:
            if X is None:
                err.new("X field is not set: please specify a parameter", self.chart)
            x_field = X
        else:
            X = x_field
        if y_field is None:
            if Y is None:
                err.new("Y field is not set: please specify a parameter", self.chart)
            y_field = Y
        else:
            Y = y_field
        if opts is not None:
            self.chart_opts = opts
        if style is not None:
            self.chart_style = style
        if label is not None:
            self.label = label
        self.x_field = x_field
        self.y_field = y_field
        self.chart_obj = self._get_chart(chart_type, x_field,
                                         y_field, style=style, opts=opts, label=label)
        if err.exists:
            err.throw()
        return self.chart_obj

    def bar(self, style=None, opts=None, label=None):
        """
        Get a bar chart
        """
        return self._get_chart("bar", style=style, opts=opts, label=label)

    def line(self, style=None, opts=None, label=None):
        """
        Get a line chart
        """
        return self._get_chart("line", style=style, opts=opts, label=label)

    def area(self, style=None, opts=None, label=None):
        """
        Get an area chart
        """
        return self._get_chart("area", style=style, opts=opts, label=label)

    def point(self, style=None, opts=None, label=None):
        """
        Get a point chart
        """
        return self._get_chart("point", style=style, opts=opts, label=label)

    def line_point(self, colors={"line": "yellow", "point": "navy"}, style=None, opts=None, label=None):
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

    def _get_chart(self, chart_type="line", x_field=None, y_field=None, style=None, opts=None, label=None):
        """
        Get a full chart object
        """
        if opts is None:
            opts = self.chart_opts
        if style is None:
            style = self.chart_style
        if x_field is None:
            x_field = self.x_field
        if y_field is None:
            y_field = self.y_field
        base_chart = self._get_base_chart(
            x_field, y_field, chart_type, label)
        chart = base_chart(plot=opts, style=style)
        return chart

    def _get_base_chart(self, x_field, y_field, chart_type="line", label=None):
        """
        Get a base chart object
        """
        args = dict(data=self.df, kdims=[x_field], vdims=[y_field])
        if label is not None:
            args["label"] = label
        else:
            if self.label is not None:
                args["label"] = self.label
        chart = None
        if chart_type == "line":
            chart = hv.Curve(**args)
        elif chart_type == "point":
            chart = hv.Scatter(**args)
        elif chart_type == "area":
            chart = hv.Area(**args)
        elif chart_type == "bar":
            chart = hv.Bars(**args)
        if chart is None:
            err.new("Chart type " + chart_type +
                    " unknown", self._get_base_chart)
        return chart
