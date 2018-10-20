# -*- coding: utf-8 -*
from altair import Chart


class Altair():
    """
    A class to handle charts with the Altair library
    """

    def __init__(self, df=None):
        """
        Initialize
        """
        self.df = df
        self.altair_encode = {}

    def aenc(self, key, value):
        """
        Add an entry to the altair encoding dict
        """
        self.altair_encode[key] = value

    def raenc(self, key):
        """
        Remove an entry from the altair encoding dict
        """
        if key in self.altair_encode:
            del self.altair_encode[key]
        else:
            self.warning("Key " + key + " not found in Altair encoding dict")

    def raencs(self):
        """
        Reset the altair encoding dict
        """
        self.altair_encode = {}

    def _altair_line_num_(self, xfield, yfield, opts, style, encode):
        """
        Get a line + text number chart
        """
        try:
            c = self._altair_chart_num_("line", xfield,
                                           yfield, opts, style, encode)
        except Exception as e:
            self.err(e, "Can not draw a line num chart")
            return
        return c

    def _altair_bar_num_(self, xfield, yfield, opts, style, encode):
        """
        Get a bar + text number chart
        """
        try:
            c = self._altair_chart_num_("bar", xfield,
                                           yfield, opts, style, encode)
        except Exception as e:
            self.err(e, "Can not draw a bar num chart")
            return
        return c

    def _altair_chart_num_(self, chart_type, xfield, yfield, opts, style2, encode):
        """
        Get a chart + text number chart
        """
        style = {**style2}
        text_color = "grey"
        if "text_color" in style:
            text_color = style["text_color"]
            del style["text_color"]
            if "text_color" in self.chart_style:
                del self.chart_style["text_color"]
        if chart_type == "line":
            c = Chart(self.df).mark_line(**style).encode(x=xfield, \
                                                y=yfield, **encode).properties(**opts)
        if chart_type == "bar":
            c = Chart(self.df).mark_bar(**style).encode(x=xfield, \
                                                y=yfield, **encode).properties(**opts)
        encoder = encode
        if "text" not in encoder:
            encoder["text"] = yfield
        if "align" not in style:
            style["align"] = "center"
        if "dy" not in style:
            style["dy"] = -5
        if "dx" not in style:
            style["dx"] = 8
        if "size" in style:
            del style["size"]
        style["color"] = text_color
        df2 = self.df.replace({yfield.split(":")[0]: {0: self.nan}})
        num = Chart(df2).mark_text(**style).encode(x=xfield, \
                                            y=yfield, **encoder).properties(**opts)
        return c + num

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
        encode = self.altair_encode
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
        elif chart_type == "line_num":
            chart = self._altair_line_num_(xfield, yfield, opts, style, encode)
        elif chart_type == "bar_num":
            chart = self._altair_bar_num_(xfield, yfield, opts, style, encode)
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

    def altair_header_(self):
        """
        Returns html script tags for Altair
        """
        header = """
        <script src="https://cdn.jsdelivr.net/npm/vega@3"></script>
        <script src="https://cdn.jsdelivr.net/npm/vega-lite@2"></script>
        <script src="https://cdn.jsdelivr.net/npm/vega-embed@3"></script>
        <style>.vega-actions {display:none}</style>
        """
        return header

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
        function showError(altel, error){
            altel.innerHTML = ('<div class="error">'
                            + '<p>JavaScript Error: ' + error.message + '</p>'
                            + "<p>This usually means there's a typo in your chart specification. "
                            + "See the javascript console for the full traceback.</p>"
                            + '</div>');
            throw error;
        };\n"""
        html += "const el_" + slug + " = document.getElementById('" + slug + "');"
        html += "vegaEmbed('#" + slug + "', spec, embed_opt)"
        html += ".catch(error => showError(el_" + slug + ", error));"
        html += '</script>'
        return html

    def _set_altair_engine(self):
        """
        Set the current chart engine to Altair
        """
        if self.engine != "altair":
            self.engine = "altair"
            self.info("Switching to the Altair engine to draw this chart")
