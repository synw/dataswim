from .bokeh import Bokeh
from .altair import Altair
from .colors import Colors


class Plot(Bokeh, Altair, Colors):
    """
    Class to handle charts
    """

    def __init__(self, df=None):
        """
        Initialize
        """
        self.df = df
        self.x = None
        self.err = None
        self.y = None
        self.chart_obj = None
        self.chart_opts = dict(width=940)
        self.chart_style = None
        self.label = None
        self.engine = "bokeh"

    def chart(self, x=None, y=None, chart_type="line", opts=None, style=None, label=None):
        """
        Get a chart
        """
        try:
            self.chart_obj = self._chart(x, y, chart_type, opts, style, label)
        except Exception as e:
            self.err(e, self.chart, "Can not create chart")

    def chart_(self, x=None, y=None, chart_type="line", opts=None, style=None, label=None):
        """
        Get a chart
        """
        try:
            return self._chart(x, y, chart_type, opts, style, label)
        except Exception as e:
            self.err(e, self.chart, "Can not create chart")

    def _chart(self, x=None, y=None, chart_type="line", opts=None, style=None, label=None):
        """
        Initialize chart options
        """
        if opts is not None:
            self.chart_opts = opts
        if style is not None:
            self.chart_style = style
        if label is not None:
            self.label = label
        self.x = x
        self.y = y
        try:
            chart_obj = self._get_chart(chart_type, x,
                                        y, style=style, opts=opts, label=label)
            return chart_obj
        except Exception as e:
            self.err(e)

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

    def _get_chart(self, chart_type, x=None, y=None, style=None, opts=None, label=None):
        """
        Get a full chart object
        """
        if x is None:
            if self.x is None:
                self.err(
                    self._get_chart, "X field is not set: please specify a parameter")
                return
            x = self.x
        if y is None:
            if self.y is None:
                self.err(
                    self._get_chart, "Y field is not set: please specify a parameter")
                return
            y = self.y
        if opts is None:
            opts = self.chart_opts
        if style is None:
            style = self.chart_style
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if self.engine == "bokeh":
            func = self._get_bokeh_chart
        elif self.engine == "altair":
            func = self._get_altair_chart
        else:
            self.err(self._get_chart, "Engine " + self.engine + " unknown")
            return
        try:
            chart = func(
                x, y, chart_type, label, opts, style)
            return chart
        except Exception as e:
            self.err(e)
