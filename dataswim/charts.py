# -*- coding: utf-8 -*-

import holoviews as hv
from goerr import err


X = None
Y = None


class Plot():
    """
    Class to handle charts
    """

    def __init__(self, df=None, db=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df
        self.x_field = None
        self.y_field = None
        self.chart_obj = None
        self.chart_opts = dict(width=940)
        self.chart_style = None
        self.label = None

    def chart(self, x_field=None, y_field=None, chart_type="line", opts=None, style=None, label=None):
        """
        Initialize chart options
        """
        if opts is not None:
            self.chart_opts = opts
        if style is not None:
            self.chart_style = style
        if label is not None:
            self.label = label
        self.x_field = x_field
        self.y_field = y_field
        try:
            self.chart_obj = self._get_chart(chart_type, x_field,
                                             y_field, style=style, opts=opts, label=label)
        except Exception as e:
            self.err(e, self.chart, "Can not chart data")

    def bar_(self, label=None, style=None, opts=None):
        """
        Get a bar chart
        """
        try:
            return self._get_chart("bar", style=style, opts=opts, label=label)
        except Exception as e:
            self.err(e, self.chart, "Can draw bar chart")

    def line_(self, label=None, style=None, opts=None):
        """
        Get a line chart
        """
        try:
            return self._get_chart("line", style=style, opts=opts, label=label)
        except Exception as e:
            self.err(e, self.line_, "Can draw line chart")

    def area_(self, label=None, style=None, opts=None):
        """
        Get an area chart
        """
        try:
            return self._get_chart("area", style=style, opts=opts, label=label)
        except Exception as e:
            self.err(e, self.area_, "Can draw area chart")

    def hist_(self, label=None, style=None, opts=None):
        """
        Get an historiogram chart
        """
        try:
            return self._get_chart("hist", style=style, opts=opts, label=label)
        except Exception as e:
            self.err(e, self.hist_, "Can draw historiogram")

    def errorbar_(self, label=None, style=None, opts=None):
        """
        Get a point chart
        """
        try:
            return self._get_chart("err", style=style, opts=opts, label=label)
        except Exception as e:
            self.err(e, self.errorbar_, "Can draw errorbar chart")

    def point_(self, label=None, style=None, opts=None):
        """
        Get a point chart
        """
        try:
            return self._get_chart("point", style=style, opts=opts, label=label)
        except Exception as e:
            self.err(e, self.point_, "Can draw point chart")

    def heatmap_(self, label=None, style=None, opts=None):
        """
        Get a heatmap chart
        """
        try:
            return self._get_chart("point", style=style, opts=opts, label=label)
        except Exception as e:
            self.err(e, self.heatmap_, "Can draw heatmap")

    def line_point_(self, label=None, style=None, opts=None, colors={"line": "yellow", "point": "navy"}):
        """
        Get a line and point chart
        """
        try:
            if style is None:
                style = self.chart_style
            style["color"] = colors["line"]
            l = self._get_chart("line", style=style, opts=opts, label=label)
            style["color"] = colors["point"]
            p = self._get_chart("point", style=style, opts=opts, label=label)
            return l * p
        except Exception as e:
            self.err(e, self.line_point_, "Can draw line_point chart")

    def opts(self, dictobj):
        """
        Add or update an option value to defaults
        """
        for k in dictobj:
            self.chart_opts[k] = dictobj[k]

    def style(self, dictobj):
        """
        Add or update a style value to defaults
        """
        for k in dictobj:
            self.chart_style[k] = dictobj[k]

    def _get_chart(self, chart_type="line", x_field=None, y_field=None, style=None, opts=None, label=None):
        """
        Get a full chart object
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
        if opts is None:
            opts = self.chart_opts
        if style is None:
            style = self.chart_style
        if x_field is None:
            x_field = self.x_field
        if y_field is None:
            y_field = self.y_field
        try:
            base_chart = self._get_base_chart(
                x_field, y_field, chart_type, label)
            chart = base_chart(plot=opts, style=style)
            return chart
        except Exception as e:
            self.err(e)

    def _get_base_chart(self, x_field, y_field, chart_type, label):
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
        try:
            if chart_type == "line":
                try:
                    chart = hv.Curve(**args)
                except Exception as e:
                    self.err(e)
            elif chart_type == "point":
                chart = hv.Scatter(**args)
            elif chart_type == "area":
                chart = hv.Area(**args)
            elif chart_type == "bar":
                chart = hv.Bars(**args)
            elif chart_type == "hist":
                chart = hv.Histogram(**args)
            elif chart_type == "err":
                chart = hv.ErrorBars(**args)
            return chart
        # BROKEN in Holoview 1.9.0
        # except DataError as e:
        #    msg = "Column not found in " + x_field + " and " + y_field
        #    self.err(e, msg)
        except Exception as e:
            self.err(e)
        if chart is None:
            self.err("Chart type " + chart_type +
                     " unknown", self._get_base_chart)
