# -*- coding: utf-8 -*
from altair import Chart
import json


class Altair():
    """
    A class to handle charts with the Altair library
    """

    def __init__(self, df=None):
        """
        Initialize
        """
        self.df = df

    def _altair_hline_(self, xfield, yfield, opts, style, encode):
        """
        Get a mean line chart
        """
        try:
            rawy = yfield
            if ":" in yfield:
                rawy = yfield.split(":")[0]
            mean = self.df[rawy].mean()
            l = []
            i = 0
            while i < len(self.df[rawy]):
                l.append(mean)
                i += 1
            self.df["Mean"] = l
            chart = Chart(self.df).mark_line(**style).encode(x=xfield, \
                                            y="Mean", **encode).properties(**opts)
            self.drop("Mean")
            return chart
        except Exception as e:
            self.err(e, "Can not draw mean line chart")

    def _get_altair_chart(self, xfield, yfield, chart_type,
                          label, opts={}, style={}, **kwargs):
        """
        Get an Altair chart object
        """
        encode = {}
        if "color" in style:
            encode["color"] = style["color"]
        chart = None
        if chart_type == "bar":
            chart = Chart(self.df).mark_bar(**style).encode(x=xfield, \
                                            y=yfield, **encode).properties(**opts)
        elif chart_type == "circle":
            chart = Chart(self.df).mark_circle(**style).encode(x=xfield, \
                                            y=yfield, **encode).properties(**opts)
        elif chart_type == "line":
            chart = Chart(self.df).mark_line(**style).encode(x=xfield, \
                                            y=yfield, **encode).properties(**opts)
        elif chart_type == "hline":
            chart = self._altair_hline_(xfield, yfield, opts, style, encode)
        elif chart_type == "point":
            chart = Chart(self.df).mark_point(**style).encode(x=xfield, \
                                            y=yfield, **encode).properties(**opts)
        elif chart_type == "area":
            chart = Chart(self.df).mark_area(**style).encode(x=xfield, \
                                            y=yfield, **encode).properties(**opts)
        elif chart_type == "heatmap":
            chart = Chart(self.df).mark_rect(**style).encode(x=xfield, \
                                            y=yfield, **encode).properties(**opts)
        elif chart_type == "text":
            chart = Chart(self.df).mark_text(**style).encode(x=xfield, \
                                            y=yfield, **encode).properties(**opts)
        elif chart_type == "square":
            chart = Chart(self.df).mark_square(**style).encode(x=xfield, \
                                                y=yfield, **encode).properties(**opts)
        elif chart_type == "tick":
            chart = Chart(self.df).mark_tick(**style).encode(x=xfield, \
                                            y=yfield, **encode).properties(**opts)
        elif chart_type == "rule":
            chart = Chart(self.df).mark_rule(**style).encode(x=xfield, \
                                            y=yfield, **encode).properties(**opts)
        return chart

    def _get_altair_html_(self, chart_obj, slug):
        """
        Get html for an Altair chart
        """
        try:
            json_data = chart_obj.to_json(indent=0)
        except Exception as e:
            self.err(e)
        html = '<div id="' + slug + '"></div>\n'
        html += '<script type="text/javascript">'
        html += 'var spec = ' + json_data.replace("\n", "") + ";"
        html += """
        var embed_opt = {"mode": "vega-lite"};
        function showError(el, error){
            el.innerHTML = ('<div class="error">'
                            + '<p>JavaScript Error: ' + error.message + '</p>'
                            + "<p>This usually means there's a typo in your chart specification. "
                            + "See the javascript console for the full traceback.</p>"
                            + '</div>');
            throw error;
        };\n"""
        html += "const el = document.getElementById('" + slug + "');"
        html += "vegaEmbed('#" + slug + "', spec, embed_opt)"
        html += ".catch(error => showError(el, error));"
        html += '</script>'
        return html

    def _set_altair_engine(self):
        """
        Set the current chart engine to Altair
        """
        if self.engine != "altair":
            self.engine = "altair"
            self.info("Switching to the Altair engine to draw this chart")
