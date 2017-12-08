import seaborn as sns


class Seaborn():
    """
    A class to handle Seaborn charts
    """

    def linear_(self, label=None, style={}, opts={}, options={}):
        """
        Returns a linear regression plot with marginal distribution
        """
        if self.x is None:
            self.err(
                self._linear_, "X field is not set: please specify a parameter")
            return
        x = self.x
        if self.y is None:
            self.err(
                self._get_linear_, "Y field is not set: please specify a parameter")
            return
            y = self.y
        if self.engine != "seaborn":
            self.engine = "seaborn"
            self.info("Switching to the Seaborn engine to draw this chart")
        color = "r"
        if not "xticks" in opts:
            if not "xticks" in self.chart_opts:
                self.err(self._linear,
                         "Please set the xticks option for this chart to work")
                return
            else:
                xticks = self.chart_opts["xticks"]
        else:
            xticks = opts["xticks"]
        if not "yticks" in opts:
            if not "yticks" in self.chart_opts:
                self.err(self._linear,
                         "Please set the yticks option for this chart to work")
                return
            else:
                yticks = self.chart_opts["yticks"]
        else:
            xticks = opts["xticks"]
        if "color" in style:
            color = style["color"]
        size = 7
        if "size" in style:
            size = style["size"]
        self.chart_type = "linear"
        try:
            sns.set(style="darkgrid", color_codes=True)
            fig = sns.jointplot(self.x, self.y, data=self.df, kind="reg",
                                xlim=xticks, ylim=yticks, color=color, size=size)
            return fig
        except Exception as e:
            self.err(e, self.linear_, "Can not draw linear regression chart")

    def _get_seaborn_chart(self, xfield, yfield, chart_type, label, opts={}, style={}, options={}, **kwargs):
        """
        Get an Seaborn chart object
        """
        # params
        opts["xfield"] = xfield
        opts["yfield"] = yfield
        opts["dataobj"] = self.df
        opts["chart_type"] = chart_type
        opts["options"] = options
        # generate
        try:
            if chart_type == "linear":
                chart_obj = self.linear_(label, style, opts, options)
            else:
                self.err(self._get_seaborn_chart, "Chart type " +
                         chart_type + " not supported with Seaborn")
                return
        except Exception as e:
            self.err(e, self._get_seaborn_chart,
                     "Can not get Altair chart object")
            return
        return chartobj
