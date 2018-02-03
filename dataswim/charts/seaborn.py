import seaborn as sns


class Seaborn():
    """
    A class to handle Seaborn charts
    """

    def residual_(self, label=None, style=None, opts=None):
        """
        Returns a Seaborn models residuals chart
        """
        opts, style = self._get_opts_seaborn(opts, style)
        color, _ = self._get_color_size(style)
        try:
            fig = sns.residplot(self.df[self.x], self.df[self.y],
                                lowess=True, color=color)
            fig = self._set_with_height(fig, opts)
            return fig
        except Exception as e:
            self.err(e, self.residual_,
                     "Can not draw models residuals chart")

    def density_(self, label=None, style=None, opts=None):
        """
        Returns a Seaborn density chart
        """
        opts, style = self._get_opts_seaborn(opts, style)
        try:
            fig = sns.kdeplot(self.df[self.x], self.df[self.y])
            fig = self._set_with_height(fig, opts)
            return fig
        except Exception as e:
            self.err(e, self.density_,
                     "Can not draw density chart")

    def distrib_(self, label=None, style=None, opts=None):
        """
        Returns a Seaborn distribution chart
        """
        opts, style = self._get_opts_seaborn(opts, style)
        color, _ = self._get_color_size(style)
        try:
            kde = False
            rug = True
            if "kde" in opts:
                kde = opts["kde"]
                rug = opts["rug"]
            fig = sns.distplot(self.df[self.x], color=color, kde=kde, rug=rug)
            fig = self._set_with_height(fig, opts)
            return fig
        except Exception as e:
            self.err(e, self.distrib_,
                     "Can not draw distribution chart")

    def linear_(self, label=None, style=None, opts=None):
        """
        Returns a Seaborn linear regression plot
        """
        opts, style = self._get_opts_seaborn(opts, style)
        xticks, yticks = self._get_ticks(opts)
        color, size = self._get_color_size(style)
        self.chart_type = "linear"
        try:
            fig = sns.lmplot(self.x, self.y, data=self.df)
            fig = self._set_with_height(fig, opts)
            return fig
        except Exception as e:
            self.err(e, self.linear_,
                     "Can not draw linear regression chart")

    def dlinear_(self, label=None, style=None, opts=None):
        """
        Returns a Seaborn linear regression plot with marginal distribution
        """
        opts, style = self._get_opts_seaborn(opts, style)
        xticks, yticks = self._get_ticks(opts)
        color, size = self._get_color_size(style)
        self.chart_type = "dlinear"
        try:
            fig = sns.jointplot(self.x, self.y, data=self.df, kind="reg",
                                xlim=xticks, ylim=yticks, color=color,
                                size=size)
            fig = self._set_with_height(fig, opts)
            return fig
        except Exception as e:
            self.err(e, self.dlinear_,
                     "Can not draw linear regression chart with distribution")

    def seaborn_bar_(self, label=None, style=None, opts=None):
        """
        Get a Seaborn bar chart
        """
        opts, style = self._get_opts_seaborn(opts, style)
        try:
            fig = sns.barplot(self.x, self.y, palette="BuGn_d")
            fig = self._set_with_height(fig, opts)
            return fig
        except Exception as e:
            self.err(e, self.seaborn_bar_,
                     "Can not get Seaborn bar chart object")

    def _get_opts_seaborn(self, _opts, _style):
        """
        Initialialize for chart rendering
        """
        opts, style = self._get_opts(_opts, _style)
        self._check_defaults()
        self._set_seaborn_engine()
        return opts, style

    def _get_seaborn_chart(self, xfield, yfield, chart_type, label,
                           opts=None, style=None, **kwargs):
        """
        Get an Seaborn chart object
        """
        try:
            opts, style = self._get_opts(opts, style)
        except Exception as e:
            self.err(e, self._get_seaborn_chart, "Can not get chart options")
        # params
        opts["xfield"] = xfield
        opts["yfield"] = yfield
        opts["dataobj"] = self.df
        opts["chart_type"] = chart_type
        # generate
        try:
            sns.set(style="darkgrid", color_codes=True)
            if chart_type == "dlinear":
                chart_obj = self.dlinear_(label, style, opts)
            elif chart_type == "linear":
                chart_obj = self.linear_(label, style, opts)
            elif chart_type == "distribution":
                chart_obj = self.distrib_(label, style, opts)
            elif chart_type == "density":
                chart_obj = self.density_(label, style, opts)
            elif chart_type == "residual":
                chart_obj = self.residual_(label, style, opts)
            elif chart_type == "bar":
                chart_obj = self.seaborn_bar_(label, style, opts)
            else:
                self.err(self._get_seaborn_chart, "Chart type " +
                         chart_type + " not supported with Seaborn")
                return
        except Exception as e:
            self.err(e, self._get_seaborn_chart,
                     "Can not get Seaborn chart object")
            return
        return chart_obj

    def _get_ticks(self, opts):
        """
        Check if xticks and yticks are set
        """
        opts, _ = self._get_opts(opts, None)
        if "xticks" not in opts:
            if "xticks" not in self.chart_opts:
                self.err(self.dlinear_,
                         "Please set the xticks option for this chart to work")
                return
            else:
                xticks = self.chart_opts["xticks"]
        else:
            xticks = opts["xticks"]
        if "yticks" not in opts:
            if "yticks"not in self.chart_opts:
                self.err(self.dlinear_,
                         "Please set the yticks option for this chart to work")
                return
            else:
                yticks = self.chart_opts["yticks"]
        else:
            yticks = opts["yticks"]
        return xticks, yticks

    def _get_color_size(self, style):
        """
        Get color and size from a style dict
        """
        color = "b"
        if "color" in style:
            color = style["color"]
        size = 7
        if "size" in style:
            size = style["size"]
        return color, size

    def _set_with_height(self, fig, opts):
        """
        Set the width and height of a Matplotlib figure
        """
        h = 5
        if "height" in opts:
            h = opts["height"]
        w = 12
        if "width" in opts:
            w = opts["width"]
        try:
            fig.figure.set_size_inches((w, h))
            return fig
        except Exception:
            try:
                fig.fig.set_size_inches((w, h))
                return fig
            except Exception as e:
                self.err(e, self._set_with_height,
                         "Can not set figure width and height from chart object")

    def _get_opts(self, opts, style):
        """
        Get default options
        """
        o = opts
        if opts is None:
            o = self.chart_opts
        s = style
        if style is None:
            s = self.chart_style
        return o, s

    def _save_seaborn_chart(self, report, folderpath):
        """
        Saves a png image of the seaborn chart
        """
        if folderpath is None:
            if self.imgs_path is None:
                self.err(self._save_seaborn_chart,
                         "Please set a path where to save images: ds.imgs_path"
                         " = '/my/path'")
                return
            path = self.imgs_path
        else:
            path = folderpath
        path = path + "/" + report["slug"] + ".png"
        try:
            try:
                #print("*** TRY", report["seaborn_chart"].figure.show())
                fig = report["seaborn_chart"].figure
                fig.savefig(path)
            except Exception as e:
                try:
                    fig = report["seaborn_chart"]
                    fig.savefig(path)
                except Exception:
                    plot = report["seaborn_chart"]
                    plot = plot.get_figure()
                    plot.savefig(path)
        except Exception as e:
            self.err(e, self._save_seaborn_chart, "Can not save Seaborn chart")
            return
        if self.autoprint is True:
            self.ok("Seaborn chart writen to " + path)

    def _set_seaborn_engine(self):
        """
        Set the current chart engine to Seaborn
        """
        if self.engine != "seaborn":
            self.engine = "seaborn"
            self.info("Switching to the Seaborn engine to draw this chart")
