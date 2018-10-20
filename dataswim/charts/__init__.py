# @PydevCodeAnalysisIgnore
import holoviews as hv
from .bokeh import Bokeh
from .altair import Altair
from .chartjs import Chartjs
from .seaborn import Seaborn
from .colors import Colors


class Plot(Bokeh, Chartjs, Seaborn, Altair, Colors):
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
        self.chart_style = {}
        self.label = None
        self.engine = "bokeh"

    def chart(self, x=None, y=None, chart_type=None, opts=None,
              style=None, label=None, options={}, **kwargs):
        """
        Get a chart
        """
        try:
            self.chart_obj = self._chart(x, y, chart_type, opts, style, label,
                                         options=options, **kwargs)
        except Exception as e:
            self.err(e, self.chart, "Can not create chart")

    def chart_(self, x=None, y=None, chart_type=None, opts=None, style=None,
               label=None, options={}, **kwargs):
        """
        Get a chart
        """
        try:
            return self._chart(x, y, chart_type, opts, style, label,
                               options=options, **kwargs)
        except Exception as e:
            self.err(e, self.chart, "Can not create chart")

    def _chart(self, x, y, chart_type, opts, style, label, options, **kwargs):
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
        if chart_type is None:
            return
        try:
            chart_obj = self._get_chart(chart_type, x, y, style=style,
                                        opts=opts, label=label,
                                        options=options, **kwargs)
            return chart_obj
        except Exception as e:
            self.err(e)

    def bar_(self, label=None, style=None, opts=None, options={}):
        """
        Get a bar chart
        """
        try:
            return self._get_chart("bar", style=style, opts=opts, label=label,
                                   options=options)
        except Exception as e:
            self.err(e, self.bar_, "Can not draw bar chart")

    def sbar_(self, stack_index=None, label=None, style=None, opts=None,
              options={}):
        """
        Get a stacked bar chart
        """
        self.opts(dict(stack_index=stack_index, color_index=stack_index))
        try:
            if stack_index is None:
                self.err(self.sbar_, "Please provide a stack index parameter")
            options["stack_index"] = stack_index
            return self._get_chart("bar", style=style, opts=opts, label=label,
                                   options=options)
        except Exception as e:
            self.err(e, self.sbar_, "Can not draw stacked bar chart")

    def quants_(self, inf, sup, chart_type="point",
                color="green"):
        """
        Draw a chart to visualize quantiles
        """
        try:
            return self._bokeh_quants(inf, sup, chart_type, color)
        except Exception as e:
            self.err(e, self.quants_, "Can not draw quantile chart")

    def line_(self, label=None, style=None, opts=None, options={}):
        """
        Get a line chart
        """
        try:
            return self._get_chart("line", style=style, opts=opts,
                                   label=label, options=options)
        except Exception as e:
            self.err(e, self.line_, "Can not draw line chart")

    def hline_(self, label=None, style=None, opts=None, options={}):
        """
        Get a mean line chart
        """
        try:
            return self._get_chart("hline", style=style, opts=opts,
                                   label=label, options=options)
        except Exception as e:
            self.err(e, self.line_, "Can not draw mean line chart")

    def sline_(self, window_size=5,
               y_label="Moving average", chart_label=None):
        """
        Get a moving average curve chart to smooth between points
        """
        options = dict(window_size=window_size, y_label=y_label)
        try:
            return self._get_chart("sline", style=self.chart_style,
                                   opts=self.chart_opts, label=chart_label,
                                   options=options)
        except Exception as e:
            self.err(e, self.sline_, "Can not draw smooth curve chart")

    def area_(self, label=None, style=None, opts=None, options={}):
        """
        Get an area chart
        """
        try:
            return self._get_chart("area", style=style, opts=opts,
                                   label=label, options=options)
        except Exception as e:
            self.err(e, self.area_, "Can not draw area chart")

    def sarea_(self, col, x=None, y=None, rsum=None, rmean=None):
        """
        Get an stacked area chart
        """
        try:
            charts = self._multiseries(col, x, y, "area", rsum, rmean)
            return hv.Area.stack(charts)
        except Exception as e:
            self.err(e, self.sarea_, "Can not draw stacked area chart")

    def hist_(self, label=None, style=None, opts=None, options={}):
        """
        Get an historiogram chart
        """
        try:
            return self._get_chart("hist", style=style, opts=opts,
                                   label=label, options=options)
        except Exception as e:
            self.err(e, self.hist_, "Can not draw historiogram")

    def errorbar_(self, label=None, style=None, opts=None, options={}):
        """
        Get a point chart
        """
        try:
            return self._get_chart("errorBar", style=style, opts=opts,
                                   label=label, options=options)
        except Exception as e:
            self.err(e, self.errorbar_, "Can not draw errorbar chart")

    def point_(self, label=None, style=None, opts=None, options={}):
        """
        Get a point chart
        """
        try:
            return self._get_chart("point", style=style, opts=opts,
                                   label=label, options=options)
        except Exception as e:
            self.err(e, self.point_, "Can not draw point chart")

    def circle_(self, label=None, style=None, opts=None, options={}):
        """
        Get a circle chart
        """
        try:
            return self._get_chart("circle", style=style, opts=opts,
                                   label=label, options=options)
        except Exception as e:
            self.err(e, self.circle_, "Can not draw circle chart")

    def square_(self, label=None, style=None, opts=None, options={}):
        """
        Get a square chart
        """
        try:
            return self._get_chart("square", style=style, opts=opts,
                                   label=label, options=options)
        except Exception as e:
            self.err(e, self.square_, "Can not draw square chart")

    def tick_(self, label=None, style=None, opts=None, options={}):
        """
        Get an tick chart
        """
        try:
            self._get_chart("tick", style=style, opts=opts,
                                   label=label, options=options)
        except Exception as e:
            self.err(e, "Can not draw tick chart")

    def rule_(self, label=None, style=None, opts=None, options={}):
        """
        Get a rule chart
        """
        try:
            return self._get_chart("rule", style=style, opts=opts,
                                   label=label, options=options)
        except Exception as e:
            self.err(e, self.rule_, "Can not draw rule chart")

    def heatmap_(self, label=None, style=None, opts=None, options={}):
        """
        Get a heatmap chart
        """
        try:
            return self._get_chart("heatmap", style=style, opts=opts,
                                   label=label, options=options)
        except Exception as e:
            self.err(e, self.heatmap_, "Can not draw heatmap")

    def lreg_(self, label=None, style=None, opts=None, options={}):
        """
        Get a linear regression chart
        """
        try:
            return self._get_chart("lreg", style=style, opts=opts,
                                   label=label, options=options)
        except Exception as e:
            self.err(e, self.rule_, "Can not draw linear regression chart")

    def line_point_(self, label=None, style=None, opts=None, options={},
                    colors={"line": "orange", "point": "#30A2DA"}):
        """
        Get a line and point chart
        """
        try:
            if style is None:
                style = self.chart_style
                if "size" not in style:
                    style["size"] = 10
            style["color"] = colors["line"]
            c = self._get_chart("line", style=style, opts=opts,
                                label=label, options=options)
            style["color"] = colors["point"]
            c2 = self._get_chart("point", style=style, opts=opts,
                                 label=label, options=options)
            return c * c2
        except Exception as e:
            self.err(e, self.line_point_, "Can not draw line_point chart")

    def mpoint_(self, col, x=None, y=None, rsum=None, rmean=None):
        """
        Splits a column into multiple series based on the column's
        unique values. Then visualize theses series in a chart.
        Parameters: column to split, x axis column, y axis column
        Optional: rsum="1D" to resample and sum data an rmean="1D"
        to mean the data
        """
        return self._multiseries(col, x, y, "point", rsum, rmean)

    def mline_(self, col, x=None, y=None, rsum=None, rmean=None):
        """
        Splits a column into multiple series based on the column's
        unique values. Then visualize theses series in a chart.
        Parameters: column to split, x axis column, y axis column
        Optional: rsum="1D" to resample and sum data an rmean="1D"
        to mean the data
        """
        return self._multiseries(col, x, y, "line", rsum, rmean)

    def mbar_(self, col, x=None, y=None, rsum=None, rmean=None):
        """
        Splits a column into multiple series based on the column's
        unique values. Then visualize theses series in a chart.
        Parameters: column to split, x axis column, y axis column
        Optional: rsum="1D" to resample and sum data an rmean="1D"
        to mean the data
        """
        return self._multiseries(col, x, y, "bar", rsum, rmean)

    def mline_point_(self, col, x=None, y=None, rsum=None, rmean=None):
        """
        Splits a column into multiple series based on the column's
        unique values. Then visualize theses series in a chart.
        Parameters: column to split, x axis column, y axis column
        Optional: rsum="1D" to resample and sum data an rmean="1D"
        to mean the data
        """
        line = self._multiseries(col, x, y, "line", rsum, rmean)
        point = self._multiseries(col, x, y, "point", rsum, rmean)
        return line * point

    def arrow_(self, xloc, yloc, text, orientation="v", arrowstyle='->'):
        """
        Returns an arrow for a chart. Params: the text, xloc and yloc are
        coordinates to position the arrow. Orientation is the way to display
        the arrow: possible values are [<, ^, >, v]. Arrow style is the
        graphic style of the arrow: possible values: [-, ->, -[, -|>, <->, <|-|>]
        """
        try:
            arrow = hv.Arrow(
                xloc,
                yloc,
                text,
                orientation,
                arrowstyle=arrowstyle)
            return arrow
        except Exception as e:
            self.err(e, self.arrow_, "Can not draw arrow chart")

    def _multiseries(self, col, x, y, ctype, rsum, rmean):
        """
        Chart multiple series from a column distinct values
        """
        self.autoprint = False
        x, y = self._check_fields(x, y)
        chart = None
        series = self.split_(col)
        for key in series:
            instance = series[key]
            if rsum is not None:
                instance.rsum(rsum, index_col=x)
            if rmean is not None:
                instance.rmean(rmean, index_col=x)
            instance.chart(x, y)
            self.scolor()
            c = None
            if ctype == "point":
                c = instance.point_(key)
            if ctype == "line":
                instance.zero_nan(y)
                c = instance.line_(key)
            if ctype == "bar":
                c = instance.bar_(key)
            if ctype == "area":
                c = instance.area_(label=key)
            if c is None:
                self.warning("Chart type " + ctype + 
                             " not supported, aborting")
                return
            if chart is None:
                chart = c
            else:
                chart = chart * c
        return chart

    def density_(self, label=None, style=None, opts=None):
        """
        Get a Seaborn density chart
        """
        try:
            return self._get_chart("density", style=style, opts=opts, label=label)
        except Exception as e:
            self.err(e, "Can not draw density chart")
            
    def dlinear_(self, label=None, style=None, opts=None):
        """
        Get a Seaborn linear + distribution chart
        """
        try:
            return self._get_chart("dlinear", style=style, opts=opts, label=label)
        except Exception as e:
            self.err(e, "Can not draw dlinear chart")
            
    def distrib_(self, label=None, style=None, opts=None):
        """
        Get a Seaborn distribution chart
        """
        try:
            return self._get_chart("distribution", style=style, opts=opts, label=label)
        except Exception as e:
            self.err(e, "Can not draw distrinution chart")

    def text_(self, label=None, style=None, opts=None):
        """
        Get an Altair text marks chart
        """
        try:
            return self._get_chart("text", style=style, opts=opts, label=label)
        except Exception as e:
            self.err(e, "Can not draw text marks chart")

    def line_num_(self, label=None, style=None, opts=None):
        """
        Get an Altair line + number marks chart
        """
        try:
            return self._get_chart("line_num", style=style, opts=opts, label=label)
        except Exception as e:
            self.err(e, "Can not draw line and numbers chart")

    def bar_num_(self, label=None, style=None, opts=None):
        """
        Get an Altair bar + number marks chart
        """
        try:
            return self._get_chart("bar_num", style=style, opts=opts, label=label)
        except Exception as e:
            self.err(e, "Can not draw line and numbers chart")

    def opt(self, name, value):
        """
        Add or update one option
        """
        self.chart_opts[name] = value

    def style(self, name, value):
        """
        Add or update one style
        """
        self.chart_style[name] = value

    def opts(self, dictobj):
        """
        Add or update options
        """
        for k in dictobj:
            self.chart_opts[k] = dictobj[k]

    def styles(self, dictobj):
        """
        Add or update styles
        """
        for k in dictobj:
            self.chart_style[k] = dictobj[k]

    def ropt(self, name):
        """
        Remove one option
        """
        try:
            del self.chart_opts[name]
        except KeyError:
            self.warning("Option " + name + " is not set")
        except:
            self.err("Can not remove option " + name)

    def rstyle(self, name):
        """
        Remove one style
        """
        try:
            del self.chart_style[name]
        except KeyError:
            self.warning("Style " + name + " is not set")
        except:
            self.err("Can not remove style " + name)

    def ropts(self):
        """
        Reset the chart options
        """
        self.chart_opts = {}

    def rstyles(self):
        """
        Reset the chart options
        """
        self.chart_style = {}

    def defaults(self):
        """
        Reset the chart options and style to defaults
        """
        self.chart_style = {}
        self.chart_opts = {}
        self.style("color", "#30A2DA")
        self.width(900)
        self.height(250)

    def color(self, val):
        """
        Change the chart's color
        """
        self.style("color", val)

    def rcolor(self):
        """
        Reset the color to the base color
        """
        self.style("color", "#30A2DA")

    def width(self, val):
        """
        Change the chart's width
        """
        self.opts(dict(width=val))

    def height(self, val):
        """
        Change the chart's height
        """
        self.opts(dict(height=val))

    def size(self, val):
        """
        Change the chart's point size
        """
        self.styles(dict(size=val))

    def _check_fields(self, x, y):
        """
        Check x and y fields parameters and initialize
        """
        if x is None:
            if self.x is None:
                self.err(
                    self._check_fields,
                    "X field is not set: please specify a parameter")
                return
            x = self.x
        if y is None:
            if self.y is None:
                self.err(
                    self._check_fields,
                    "Y field is not set: please specify a parameter")
                return
            y = self.y
        return x, y

    def _get_chart(self, chart_type, x=None, y=None, style=None, opts=None,
                   label=None, options={}, **kwargs):
        """
        Get a full chart object
        """
        sbcharts = ["density", "distribution", "dlinear"]
        acharts = ["tick", "circle", "text", "line_num", "bar_num"]
        if chart_type in sbcharts:
            self._set_seaborn_engine()
        if chart_type in acharts:
            self._set_altair_engine()
        if chart_type != "sline":
            x, y = self._check_fields(x, y)
        if opts is None:
            opts = self.chart_opts
        if style is None:
            style = self.chart_style
        if self.engine == "bokeh":
            func = self._get_bokeh_chart
        elif self.engine == "altair":
            func = self._get_altair_chart
        elif self.engine == "chartjs":
            func = self._get_chartjs_chart
        elif self.engine == "seaborn":
            func = self._get_seaborn_chart
        else:
            self.err("Engine " + self.engine + " unknown")
            return
        try:
            chart = func(
                x, y, chart_type, label, opts, style,
                options=options, **kwargs)
            return chart
        except Exception as e:
            self.err(e)

    def _check_defaults(self, x_only=True):
        """
        Checks if charts defaults are set
        """
        if self.x is None:
            self.err(self._check_defaults,
                     "X field is not set: please specify a parameter")
            return
        if x_only is True:
            return
        if self.y is None:
            self.err(self._check_defaults,
                     "Y field is not set: please specify a parameter")
            return
