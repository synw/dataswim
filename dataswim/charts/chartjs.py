import uuid
from chartjspy import chart


class Chartjs():
    """
    A class to handle charts with the Chartjs library
    """

    def _get_chartjs_chart(self, xcol, ycol, chart_type, label=None, opts={}, style={}, options={}, **kwargs):
        """
        Get Chartjs html
        """
        try:
            xdata = list(self.df[xcol])
        except Exception as e:
            self.err(e, self._get_chartjs_chart,
                     "Can not get data for y field ", ycol)
            return
        try:
            if type(ycol) != list:
                ydata = dict(name="dataset", data=list(self.df[ycol]))
            else:
                ydata = {}
                for col in ycol:
                    ydata[col] = list(self.df[col])
        except Exception as e:
            self.err(e, self._get_chartjs_chart,
                     "Can not get data for x field ", xcol)
            return
        try:
            slug = str(uuid.uuid4())
            html = chart.get(slug, xdata, ydata, label,
                             opts, style, chart_type, **kwargs)
            return html
        except Exception as e:
            self.err(e, self._get_chartjs_chart, "Can not get chart")
