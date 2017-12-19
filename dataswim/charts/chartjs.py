import uuid
from chartjspy import chart


class Chartjs():
    """
    A class to handle charts with the Chartjs library
    """

    def radar_(self, label=None, style=None, opts=None, options={}):
        """
        Get a radar chart
        """
        try:
            return self._get_chart("radar", style=style, opts=opts, label=label, options=options)
        except Exception as e:
            self.err(e, self.radar_, "Can not draw radar chart")

    def _get_chartjs_chart(self, xcol, ycol, chart_type, label=None, opts={},
                           style={}, options={}, **kwargs):
        """
        Get Chartjs html
        """
        try:
            xdata = list(self.df[xcol])
        except Exception as e:
            self.err(e, self._get_chartjs_chart,
                     "Can not get data for x field ", ycol)
            return
        if label is None:
            label = "Data"
        try:
            if type(ycol) != list:
                ydata = [dict(name=label, data=list(self.df[ycol]))]
            else:
                ydata = []
                for col in ycol:
                    y = {}
                    y["name"] = col
                    y["data"] = list(self.df[col])
                    ydata.append(y)
        except Exception as e:
            self.err(e, self._get_chartjs_chart,
                     "Can not get data for y field ", xcol)
            return
        try:
            slug = str(uuid.uuid4())
            html = chart.get(slug, xdata, ydata, label,
                             opts, style, chart_type, **kwargs)
            return html
        except Exception as e:
            self.err(e, self._get_chartjs_chart, "Can not get chart")

    def chartjs_header_(self):
        """
        Returns html script tags for Chartjs
        """
        header = """
		<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.1/Chart.bundle.min.js"></script>
		"""
        return header
