# -*- coding: utf-8 -*-

import pytablewriter
import deepdish as dd


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

    def to_h5_(self, filepath):
        """
        Export the main dataframe as Hdf5 file
        """
        try:
            if self.autoprint is True:
                self.start("Saving data to Hdf5...")
            dd.io.save(filepath, self.df)
            if self.autoprint is True:
                self.end("Finished saving Hdf5 data")
        except Exception as e:
            self.err("data.Export.to_h5_", e)
            return

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
        writer.from_dataframe(self.df)
        writer.open(filepath)
        writer.make_worksheet(title)
        writer.write_table()
        writer.close()
        if self.autoprint is True:
            self.ok("File exported to", filepath)

    def to_csv(self, filepath, index=False, **args):
        """
        Saves the main dataframe to a csv file
        """
        if self.datapath is not None:
            if filepath.startswith("/") is False and \
                    filepath.startswith(".") is False:
                filepath = self.datapath + "/" + filepath
        self.df.to_csv(filepath, encoding='utf-8', index=index, **args)
        if self.autoprint is True:
            self.ok("Data exported to", filepath)

    def to_records_(self):
        """
        Returns a list of dictionary records from the main dataframe
        """
        try:
            dic = self.df.to_dict(orient="records")
            return dic
        except Exception as e:
            self.err(e, self.to_records_, "Can not create records")

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
