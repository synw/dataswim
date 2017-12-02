from pychartjs import chart


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
            ydata = list(self.df[ycol])
        except Exception as e:
            self.err(e, self._get_chartjs_chart,
                     "Can not get data for x field ", xcol)
            return
        try:
            if chart_type == "bar":
                html = chart.bar("slug", xdata, ydata, label,
                                 opts, style, **kwargs)
                return html
        except Exception as e:
            self.err(e, self._get_chartjs_chart, "Can not get chart")
