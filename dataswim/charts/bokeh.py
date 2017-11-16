import holoviews as hv


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

    def _get_bokeh_chart(self, x_field, y_field, chart_type, label, opts, style):
        """
        Get a chart object
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
            endchart = chart(plot=opts, style=style)
            return endchart
        # BROKEN in Holoview 1.9.0
        # except DataError as e:
        #    msg = "Column not found in " + x_field + " and " + y_field
        #    self.err(e, msg)
        # TODO : check for column errors
        except Exception as e:
            self.err(e)
        if chart is None:
            self.err("Chart type " + chart_type +
                     " unknown", self._get_bokeh_chart)
