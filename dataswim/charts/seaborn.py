import seaborn as sns


class Seaborn():
    """
    A class to handle Seaborn charts
    """

    def residual_(self, label=None, style={}, opts={}, options={}):
        """
        Returns a Seaborn models residuals chart
        """
        self._check_defaults(x_only=True)
        self._set_seaborn_engine()
        color, _ = self._get_color_style(style)
        try:
            fig = sns.residplot(self.df[self.x], self.df[self.y],
                                lowess=True, color=color)
            return fig
        except Exception as e:
            self.err(e, self.residual_,
                     "Can not draw models residuals chart")

    def density_(self, label=None, style={}, opts={}, options={}):
        """
        Returns a Seaborn density chart
        """
        self._check_defaults(x_only=True)
        self._set_seaborn_engine()
        try:
            fig = sns.kdeplot(self.df[self.x], self.df[self.y])
            return fig
        except Exception as e:
            self.err(e, self.density_,
                     "Can not draw density chart")

    def distrib_(self, label=None, style={}, opts={}, options={}):
        """
        Returns a Seaborn distribution chart
        """
        self._check_defaults(x_only=True)
        self._set_seaborn_engine()
        color, _ = self._get_color_style(style)
        try:
            fig = sns.distplot(self.df[self.x], color=color)
            return fig
        except Exception as e:
            self.err(e, self.distrib_,
                     "Can not draw distribution chart")

    def linear_(self, label=None, style={}, opts={}, options={}):
        """
        Returns a Seaborn linear regression plot
        """
        self._check_defaults()
        self._set_seaborn_engine()
        xticks, yticks = self._get_ticks(opts)
        color, size = self._get_color_style(style)
        self.chart_type = "linear"
        try:
            fig = sns.lmplot(self.x, self.y, data=self.df)
            return fig
        except Exception as e:
            self.err(e, self.linear_,
                     "Can not draw linear regression chart")

    def dlinear_(self, label=None, style={}, opts={}, options={}):
        """
        Returns a Seaborn linear regression plot with marginal distribution
        """
        self._check_defaults()
        self._set_seaborn_engine()
        xticks, yticks = self._get_ticks(opts)
        color, size = self._get_color_style(style)
        self.chart_type = "linear"
        try:
            fig = sns.jointplot(self.x, self.y, data=self.df, kind="reg",
                                xlim=xticks, ylim=yticks, color=color, size=size)
            return fig
        except Exception as e:
            self.err(e, self.dlinear_,
                     "Can not draw linear regression chart with distribution")

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
        sns.set(style="darkgrid", color_codes=True)
        # generate
        try:
            if chart_type == "dlinear":
                chart_obj = self.dlinear_(label, style, opts, options)
            elif chart_type == "linear":
                chart_obj = self.linear_(label, style, opts, options)
            elif chart_type == "distribution":
                chart_obj = self.distrib_(label, style, opts, options)
            elif chart_type == "density":
                chart_obj = self.density_(label, style, opts, options)
            elif chart_type == "residual":
                chart_obj = self.residual_(label, style, opts, options)
            else:
                self.err(self._get_seaborn_chart, "Chart type " +
                         chart_type + " not supported with Seaborn")
                return
        except Exception as e:
            self.err(e, self._get_seaborn_chart,
                     "Can not get Altair chart object")
            return
        return chartobj

    def _get_ticks(self, opts):
        """
        Check if xticks and yticks are set
        """
        if not "xticks" in opts:
            if not "xticks" in self.chart_opts:
                self.err(self.dlinear_,
                         "Please set the xticks option for this chart to work")
                return
            else:
                xticks = self.chart_opts["xticks"]
        else:
            xticks = opts["xticks"]
        if not "yticks" in opts:
            if not "yticks" in self.chart_opts:
                self.err(self.dlinear_,
                         "Please set the yticks option for this chart to work")
                return
            else:
                yticks = self.chart_opts["yticks"]
        else:
            xticks = opts["xticks"]
        return xticks, yticks

    def _get_color_style(self, style_):
        """
        Get color and style for a Seaborn chart
        """
        color = "b"
        if "color" in style_:
            color = style_["color"]
        size = 7
        if "size" in style_:
            size = style_["size"]
        return color, size

    def _set_seaborn_engine(self):
        """
        Set the current chart engine to Seaborn
        """
        if self.engine != "seaborn":
            self.engine = "seaborn"
            self.info("Switching to the Seaborn engine to draw this chart")
