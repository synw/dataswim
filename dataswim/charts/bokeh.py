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

    def bokeh_header_(self):
        """
        Returns html script tags for Bokeh
        """
        header = """
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/bokeh/0.12.10/bokeh.min.js"></script>         
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/bokeh/0.12.10/bokeh.min.js.map"></script>
        <script type="text/javascript">
            Bokeh.set_log_level("info");
        </script>
        """
        return header

    def _get_bokeh_chart(self, x_field, y_field, chart_type, label, opts, style):
        """
        Get a Bokeh chart object
        """
        if type(x_field) == list:
            kdims = x_field
        else:
            kdims = [x_field]
        if type(y_field) == list:
            vdims = y_field
        else:
            vdims = [y_field]
        args = dict(data=self.df, kdims=kdims, vdims=vdims)
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
            endchart = chart(plot=opts, style=style)
            return endchart
        except DataError as e:
            msg = "Column not found in " + x_field + " and " + y_field
            self.err(e, self._get_bokeh_chart, msg)
        except Exception as e:
            self.err(e)
        if chart is None:
            self.err("Chart type " + chart_type +
                     " unknown", self._get_bokeh_chart)

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
