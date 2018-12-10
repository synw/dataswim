import numpy
import pytablewriter
import deepdish as dd


class Export():
    """
    Class to handle data exportation
    """

    def to_html_(self) -> str:
        """Convert the main dataframe to html

        :return: html data
        :rtype: str

        :example: ``ds.to_html_()``
        """
        try:
            renderer = pytablewriter.HtmlTableWriter
            data = self._build_export(renderer)
            return data
        except Exception as e:
            self.err(e, "Can not convert data to html")

    def to_json_(self) -> str:
        """Convert the main dataframe to json

        :return: json data
        :rtype: str

        :example: ``ds.to_json_()``
        """
        try:
            renderer = pytablewriter.JsonTableWriter
            data = self._build_export(renderer)
            return data
        except Exception as e:
            self.err(e, "Can not convert data to json")

    def to_javascript_(self, table_name: str="data") -> str:
        """Convert the main dataframe to javascript code

        :param table_name: javascript variable name, defaults to "data"
        :param table_name: str, optional
        :return: a javascript constant with the data
        :rtype: str

        :example: ``ds.to_javastript_("myconst")``
        """
        try:
            renderer = pytablewriter.JavaScriptTableWriter
            data = self._build_export(renderer, table_name)
            return data
        except Exception as e:
            self.err(e, "Can not convert data to javascript code")

    def to_markdown_(self) -> str:
        """Convert the main dataframe to markdown

        :return: markdown data
        :rtype: str

        :example: ``ds.to_markdown_()``
        """
        try:
            renderer = pytablewriter.MarkdownTableWriter
            data = self._build_export(renderer)
            return data
        except Exception as e:
            self.err(e, "Can not convert data to markdown")

    def to_rst_(self) -> str:
        """Convert the main dataframe to restructured text

        :return: rst data
        :rtype: str

        :example: ``ds.to_rst_()``
        """
        try:
            renderer = pytablewriter.RstGridTableWriter
            data = self._build_export(renderer)
            return data
        except Exception as e:
            self.err(e, "Can not convert data to restructured text")

    def to_python_(self, table_name: str="data") -> list:
        """Convert the main dataframe to python a python list

        :param table_name: python variable name, defaults to "data"
        :param table_name: str, optional
        :return: a python list of lists with the data
        :rtype: str

        :example: ``ds.to_python_("myvar")``
        """
        try:
            renderer = pytablewriter.PythonCodeTableWriter
            data = self._build_export(renderer, table_name)
            return data
        except Exception as e:
            self.err(e, "Can not convert data to python list")

    def to_numpy_(self, table_name: str="data") -> numpy.array:
        """Convert the main dataframe to a numpy array

        :param table_name: name of the python variable, defaults to "data"
        :param table_name: str, optional
        :return: a numpy array
        :rtype: np.array

        :example: ``ds.to_numpy_("myvar")``
        """
        try:
            renderer = pytablewriter.NumpyTableWriter
            data = self._build_export(renderer, table_name)
            return data
        except Exception as e:
            self.err(e, "Can not convert data to numpy array")

    def to_records_(self) -> dict:
        """Returns a list of dictionary records from the main dataframe

        :return: a python dictionnary with the data
        :rtype: str

        :example: ``ds.to_records_()``
        """
        try:
            dic = self.df.to_dict(orient="records")
            return dic
        except Exception as e:
            self.err(e, "Can not convert data to records")

    def to_csv(self, filepath: str, index: bool=False, **kwargs):
        """Write the main dataframe to a csv file

        :param filepath: path of the file to save
        :type filepath: str
        :param index: [description], defaults to False
        :param index: bool, optional
        :param \*args: arguments to pass to ``pd.to_csv``

        :example: ``ds.to_csv_("myfile.csv", header=false)``
        """
        try:
            self.start("Saving data to "+filepath + " ...")
            if self.datapath is not None:
                if filepath.startswith("/") is False and \
                        filepath.startswith(".") is False:
                    filepath = self.datapath + "/" + filepath
            self.df.to_csv(filepath, encoding='utf-8', index=index, **kwargs)
            self.end("Data exported to", filepath)
        except Exception as e:
            self.err(e, "Can not convert data to csv")

    def to_excel(self, filepath: str, title: str):
        """Write the main dataframe to an Excell file

        :param filepath: path of the Excel file to write
        :type filepath: str
        :param title: Title of the stylesheet
        :type title: str

        :example: ``ds.to_excel_("./myfile.xlsx", "My data")``
        """
        try:
            self.start("Saving data to Excell file: "+filepath + " ...")
            writer = pytablewriter.ExcelXlsxTableWriter()
            writer.from_dataframe(self.df)
            writer.open(filepath)
            writer.make_worksheet(title)
            writer.write_table()
            writer.close()
            self.end("File exported to", filepath)
        except Exception as e:
            self.err(e, "Can not convert data to Excel")

    def to_hdf5(self, filepath: str):
        """Write the main dataframe to Hdf5 file

        :param filepath: path where to save the file
        :type filepath: str

        :example: ``ds.to_hdf5_("./myfile.hdf5")``
        """
        try:
            self.start("Saving data to Hdf5...")
            dd.io.save(filepath, self.df)
            self.end("Finished saving Hdf5 data")
        except Exception as e:
            self.err(e, "Can not convert data to Hdf5")

    def _build_export(self, renderer, table_name=None):
        writer = renderer()
        writer.from_dataframe(self.df)
        if table_name is not None:
            writer.table_name = table_name
        data = writer.write_table()
        return data
