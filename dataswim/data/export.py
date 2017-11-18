# -*- coding: utf-8 -*-

import pytablewriter


class Export():
    """
    Class to handle data exportation
    """

    def to_html_(self):
        """
        Exports the main dataframe to html
        """
        renderer = pytablewriter.HtmlTableWriter
        data = self._build_export(renderer)
        return data

    def to_json_(self):
        """
        Exports the main dataframe to json
        """
        renderer = pytablewriter.JsonTableWriter
        data = self._build_export(renderer)
        return data

    def to_markdown_(self):
        """
        Exports the main dataframe to markdown
        """
        renderer = pytablewriter.MarkdownTableWriter()
        data = self._build_export(renderer)
        return data

    def to_rst_(self):
        """
        Exports the main dataframe to restructured text
        """
        renderer = pytablewriter.RstGridTableWriter
        data = self._build_export(renderer)
        return data

    def to_javascript_(self, table_name="table"):
        """
        Exports the main dataframe to javascript
        """
        renderer = pytablewriter.JavaScriptTableWriter
        data = self._build_export(renderer, table_name)
        return data

    def to_python_(self, table_name="table"):
        """
        Exports the main dataframe to python code
        """
        renderer = pytablewriter.PythonCodeTableWriter
        data = self._build_export(renderer, table_name)
        return data

    def to_numpy_(self, table_name="table"):
        """
        Exports the main dataframe to a numpy array
        """
        renderer = pytablewriter.NumpyTableWriter
        data = self._build_export(renderer, table_name)
        return data

    def to_excell(self, filepath, title):
        """
        Writes the main dataframe to an Excell file
        """
        writer = pytablewriter.ExcelXlsxTableWriter()
        writer.open(filepath)
        writer.make_worksheet(title)
        writer.write_table_iter()
        writer.close()
        if self.autoprint is True:
            self.ok("File exported to", filepath)

    def to_csv(self, filepath, index=False, **args):
        """
        Saves the main dataframe to a csv file
        """
        self.df.to_csv(filepath, encoding='utf-8', index=index, **args)
        if self.autoprint is True:
            self.ok("Data exported to", filepath)

    def _build_export(self, renderer, table_name=None):
        """
        Builds an export with a renderer
        """
        writer = renderer()
        writer.from_dataframe(self.df)
        if table_name is not None:
            writer.table_name = table_name
        data = writer.write_table()
        return data
