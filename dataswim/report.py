import os
from IPython.core.display import display, HTML


class Report():
    """
    Class to handle reporting
    """

    def __init__(self, df=None):
        """
        Initialize
        """
        self.engine = "bokeh"
        self.header = self._header
        self.footer = self._footer
        self.reports = []
        self.report_path = None
        self.report_engines = [self.engine]

    def stack(self, slug, chart_obj=None, title=None):
        """
        Get the html for a chart and store it
        """
        if chart_obj is None:
            if self.chart_obj is None:
                self.err(
                    self.stack,
                    "No chart object set: please provide one in parameters")
                return
            chart_obj = self.chart_obj
        try:
            seaborn_chart = None
            if self.engine == "chartjs":
                html = chart_obj
            elif self.engine == "seaborn":
                html = ""
                seaborn_chart = chart_obj
            else:
                html = self.get_html(chart_obj, slug)
            if html is None and seaborn_chart is None:
                self.err(
                    self.stack, "Can not stack: empty html reveived for " + 
                    str(chart_obj), "-", slug)
                return
            report = dict(slug=slug, html=html)
            if seaborn_chart is not None:
                report["seaborn_chart"] = seaborn_chart
            if self.engine not in self.report_engines:
                self.report_engines.append(self.engine)
            self.reports.append(report)
        except Exception as e:
            self.err(e, self.stack, "Can not stack report")
            return
        self.ok("Stacked report", slug)

    def to_file(self, slug, folderpath=None, header=None, footer=None):
        """
        Writes the html report to a file from the report stack
        """
        if folderpath is None:
            if self.report_path is None:
                self.err(
                    "Please set the report_path parameter or pass a path in arguments")
                return
            folderpath = self.report_path
        else:
            self.report_path = folderpath
        html = self._get_header(header)
        if html is None or html == "":
            self.err(self.to_file, "Can not get html header")
        for report in self.reports:  
            if "html" not in report:
                self.err("No html for report " + report)
                self.reports = self.report_engines = []
                return
            html += report["html"]
        html += self._get_footer(footer)
        try:
            path = self._write_file(slug, folderpath, html)
            path = "file://" + path
        except Exception as e:
            self.err(e, self.to_file, "Can not save report to file")
            return
        self.reports = []
        self.report_engines = []
        if self.notebook is True:
            link = '<a href="' + path + '" target="_blank">' + path + '</a>'
            return display(HTML(link))

    def to_files(self, folderpath=None):
        """
        Writes the html report to one file per report
        """
        if len(self.reports) == 0:
            self.warning("No charts to save. Use stack to add charts for saving")
            return
        if folderpath is None:
            if self.report_path is None and "seaborn" \
                    not in self.report_engines:
                self.err("No folder path set for reports: please provide "
                         "one as argument or set ds.report_path")
                return
            folderpath = self.report_path
        else:
            if folderpath.startswith('/') or folderpath.startswith("."):
                pass
            else:
                folderpath = self.report_path + "/" + folderpath
        try:
            for report in self.reports:
                if "html" not in report:
                    self.err("No html for report " + report)
                    self.reports = self.report_engines = []
                    return
                if "seaborn_chart" in report:
                    if folderpath is None and self.static_path is None:
                        self.err("Please provide a folder path or set the "
                                 "static_path property")
                        return
                    self._save_seaborn_chart(report, self.static_path)
                else:
                    html = report["html"]
                    self._write_file(report["slug"], folderpath, html)
            self.reports = []
            self.report_engines = []
        except Exception as e:
            self.err(e, self.to_files, "Can not save reports to files")
            return
        self.ok("Data writen to files")

    def get_html(self, chart_obj=None, slug=None):
        """
        Get the html and script tag for a chart
        """
        if chart_obj is None:
            if self.chart_obj is None:
                self.err(
                    "No chart object registered, please provide "
                    "one in parameters"
                )
                return
            chart_obj = self.chart_obj
        try:
            if self.engine == "bokeh":
                html = self._get_bokeh_html(chart_obj)
                if html is None:
                    self.err("No html returned for " + str(chart_obj))
                return html
            elif self.engine == "altair":
                html = self._get_altair_html_(chart_obj, slug)
                if html is None:
                    self.err("No html returned for " + str(chart_obj))
                return html
            else:
                self.err("Chart engine " + self.engine + " unknown")
                return
        except Exception as e:
            self.err(e, "Can not get html from chart object")

    def _get_header(self, header):
        """
        Gets the html header
        """
        if header is None:
            html = self.header()
        else:
            html = header
        return html

    def _get_footer(self, footer):
        """
        Gets the html footer
        """
        if footer is None:
            html = self.footer()
        else:
            html = footer
        return html

    def _write_file(self, slug, folderpath, html):
        """
        Writes a chart's html to a file
        """
        # check directories
        if not os.path.isdir(folderpath):
            try:
                os.makedirs(folderpath)
                self.info("Creating directory " + folderpath)
            except Exception as e:
                self.err(e)
                return
        # construct file path
        filepath = folderpath + "/" + slug + ".html"
        # write the file
        try:
            filex = open(filepath, "w")
            filex.write(html)
            filex.close()
            if self.notebook is False:
                self.ok("File written to", filepath)
            else:
                html = '<a href="' + filepath + '">' + filepath + '</a>'
                self.html("File written to", html)
        except Exception as e:
            self.err(e)
        return filepath

    def _header(self):
        """
        Default html header
        """
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Report</title>
        """
        if "bokeh" in self.report_engines:
            html += self.bokeh_header_()
        if "altair" in self.report_engines:
            html += self.altair_header_()
        if "chartjs" in self.report_engines:
            html += self.chartjs_header_()
        html += """
        </head>
        <body>
        """
        return html

    def _footer(self):
        """
        Default html footer
        """
        return "</body>\n</html>"
