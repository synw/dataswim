# -*- coding: utf-8 -*-

import os
import holoviews as hv
from bokeh.embed import components
from goerr import err


renderer = hv.renderer('bokeh')


class Report():
    """
    Class to handle reporting
    """

    def stack(self, slug, title, chart_obj=None):
        """
        Get the html for a chart and store it
        """
        script, html = self.get_html(chart_obj)
        title = "<h3>" + title + "</h3>"
        report = dict(slug=slug, title=title, html=script + html)
        self.reports.append(report)

    def csv(self, path):
        """
        Saves the main dataframe to a csv file
        """
        self.df.to_csv(path, encoding='utf-8')

    def file(self, slug, folderpath=None, p=True):
        """
        Writes the html report to a file from the report stack
        """
        if folderpath is None:
            folderpath = self.report_path
        else:
            self.report_path = folderpath
        html = self._header()
        for report in self.reports:
            html += report["title"] + report["html"]
        html += self._footer()
        self._write_file(slug, folderpath, html, p)
        self.reports = []

    def files(self, folderpath=None, p=True):
        """
        Writes the html report to one file per report
        """
        if folderpath is None:
            folderpath = self.report_path
        else:
            self.report_path = folderpath
        for report in self.reports:
            html = report["title"] + report["html"]
            self._write_file(report["slug"], folderpath, html, p)
        self.reports = []

    def get_html(self, chart_obj=None):
        """
        Get the html and script tag for a chart
        """
        if chart_obj is None:
            chart_obj = self.chart_obj
        p = renderer.get_plot(chart_obj).state
        script, div = components(p)
        return script, div

    def _write_file(self, slug, folderpath, html, p=True):
        """
        Writes a chart's html to a file
        """
        # check directories
        if not os.path.isdir(folderpath):
            try:
                os.makedirs(folderpath)
            except Exception as e:
                err.new(e)
        # construct file path
        filepath = folderpath + "/" + slug + ".html"
        #~ write the file
        try:
            filex = open(filepath, "w")
            filex.write(html)
            filex.close()
            if p is True:
                print("File written to", filepath)
        except Exception as e:
            err.new(e)

    def _header(self):
        return """ 
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Test</title>   
            <link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-0.12.9.min.css" type="text/css" />           
            <script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-0.12.9.min.js"></script>
            <script type="text/javascript">
                Bokeh.set_log_level("info");
            </script>
        </head>
        <body>
        """

    def _footer(self):
        return "</body>\n</html>"
