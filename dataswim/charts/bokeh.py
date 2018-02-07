import holoviews as hv
from bokeh.embed import components
from holoviews.core.data.interface import DataError


bokeh_renderer = hv.renderer('bokeh')


class Bokeh():
    """
    A class to handle charts with the Bokeh library
    """

    def __init__(self, df=None, db=None):
        """
        Initialize
        """
        self.df = df
        self.x_field = None
        self.y_field = None
        self.chart_obj = None
        self.chart_opts = dict(width=940)
        self.chart_style = None
        self.label = None
        self.engine = "bokeh"

    def ndlayout_(self, dataset, kdims, cols=3):
        """
        Create a Holoview NdLayout from a dictionnary of chart objects
        """
        try:
            return hv.NdLayout(dataset, kdims=kdims).cols(cols)
        except Exception as e:
            self.err(e, self.layout_, "Can not create layout")

    def layout_(self, chart_objs, cols=3):
        """
        Returns a Holoview Layout from chart objects
        """
        try:
            return hv.Layout(chart_objs).cols(cols)
        except Exception as e:
            self.err(e, self.layout_, "Can not build layout")

    def bokeh_header_(self):
        """
        Returns html script tags for Bokeh
        """
        header = """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bokeh/0.12.11/bokeh.css" />
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/bokeh/0.12.11/bokeh.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/bokeh/0.12.11/bokeh.min.js.map"></script>
        <script type="text/javascript">
            Bokeh.set_log_level("info");
        </script>
        """
        return header

    def hline_(self, col, label=None):
        """
        Returns an horizontal line from a column mean value
        """
        c = hv.HLine(self.df[col].mean())
        return c

    def _bokeh_quants(self, inf, sup, chart_type, color):
        """
        Draw a chart to visualize quantiles
        """
        try:
            ds2 = self.clone_()
            qi = ds2.df[ds2.y].quantile(inf)
            qs = ds2.df[ds2.y].quantile(sup)
            ds2.add("sup", qs)
            ds2.add("inf", qi)
            ds2.chart(ds2.x, ds2.y)
            if chart_type == "point":
                c = ds2.point_()
            elif chart_type == "line_point":
                c = ds2.line_point_()
            else:
                c = ds2.line_()
            ds2.color(color)
            ds2.chart(ds2.x, "sup")
            c2 = ds2.line_()
            ds2.chart(ds2.x, "inf")
            c3 = ds2.line_()
            return c * c2 * c3
        except Exception as e:
            self.err(e, self._bokeh_quants, "Can not draw quantile chart")

    def _get_bokeh_chart(self, x_field, y_field, chart_type,
                         label, opts, style, options={}, **kwargs):
        """
        Get a Bokeh chart object
        """
        if isinstance(x_field, list):
            kdims = x_field
        else:
            kdims = [x_field]
        if isinstance(y_field, list):
            vdims = y_field
        else:
            vdims = [y_field]
        args = kwargs
        args["data"] = self.df
        args["kdims"] = kdims
        args["vdims"] = vdims
        if label is not None:
            args["label"] = label
        else:
            if self.label is not None:
                args["label"] = self.label
        chart = None
        try:
            if chart_type == "line":
                chart = hv.Curve(**args)
            elif chart_type == "point":
                chart = hv.Scatter(**args)
            elif chart_type == "area":
                chart = hv.Area(**args)
            elif chart_type == "bar":
                chart = hv.Bars(**args)
            elif chart_type == "hist":
                chart = hv.Histogram(**args)
            elif chart_type == "errorBar":
                chart = hv.ErrorBars(**args)
            endchart = chart(plot=opts, style=style)
            return endchart
            if chart is None:
                self.err("Chart type " + chart_type +
                         " unknown", self._get_bokeh_chart)
                return
        except DataError as e:
            msg = "Column not found in " + x_field + " and " + y_field
            self.err(e, self._get_bokeh_chart, msg)
        except Exception as e:
            self.err(e)

    def _get_bokeh_html(self, chart_obj):
        """
        Get the html for a Bokeh chart
        """
        global bokeh_renderer
        try:
            renderer = bokeh_renderer
            p = renderer.get_plot(chart_obj).state
            script, div = components(p)
            return script + "\n" + div

        except Exception as e:
            self.err(e, self._get_bokeh_html,
                     "Can not get html from the Bokeh rendering engine")
