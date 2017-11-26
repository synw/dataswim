from goerr import err
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

    def altair_header_(self):
        """
        Returns html script tags for Altair
        To get the right Vega Lite library versions use this link:
        https://github.com/synw/django-chartflo/blob/master/chartflo/static/js/vegalite/
        """
        header = """
        <script src="https://rawgit.com/synw/django-chartflo/master/chartflo/static/js/vegalite/vega.js" charset="utf-8"></script>
        <script src="https://rawgit.com/synw/django-chartflo/master/chartflo/static/js/vegalite/vega-lite.js" charset="utf-8"></script>
        <script src="https://rawgit.com/synw/django-chartflo/master/chartflo/static/js/vegalite/vega-embed.js" charset="utf-8"></script>
        <style>.vega-embed canvas {max-width:100%;}</style>
        """
        return header

    def _get_altair_chart(self, xfield, yfield, chart_type, label, opts={}, style={}):
        """
        Get an Altair chart object
        """
        chart = ChartsGenerator()
        # params
        opts["xfield"] = xfield
        opts["yfield"] = yfield
        opts["dataobj"] = self.df
        opts["chart_type"] = chart_type
        # generate
        try:
            chartobj = chart.serialize(**opts)
        except Exception as e:
            self.err(e, self._get_altair_chart,
                     "Can not get Altair chart object")
            return
        return chartobj

    def _get_altair_html(self, chart_obj, slug):
        """
        Get the html for an Altair chart
        """
        global renderer
        try:
            chart = ChartsGenerator()
            html = chart.html(slug, None, chart_obj)
            if err.exists:
                if self.errors_handling == "exceptions":
                    err.throw()
            return html
        except Exception as e:
            self.err(e, self._get_altair_html,
                     "Can not get html from the Altair rendering engine")
