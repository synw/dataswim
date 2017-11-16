from gencharts import ChartsGenerator


class Altair():
    """
    A class to handle charts with the Altair library
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

    def _get_altair_chart(self, xfield, yfield, chart_type, label, opts, style):
        """
        Get a chart object
        """
        chart = ChartsGenerator()
        # params
        opts["xfield"] = xfield
        opts["yfield"] = yfield
        opts["dataobj"] = self.df
        opts["chart_type"] = chart_type
        # generate
        try:
            chart.serialize(**opts)
            chartobj = chart.serialize(**opts)
        except Exception as e:
            self.err(e, self._get_altair_chart, "Can not get chart object")
            return
        return chartobj
