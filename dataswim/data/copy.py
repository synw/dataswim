from ..errors import Error
from ..messages import Message


class Copy(Error, Message):
	
    def _duplicate_(self, df=None, db=None, quiet=True):
        try:
            if db is None:
                db = self.db
            if df is None:
                if self.df is None:
                    self.err("The main dataframe is empty and no dataframe"
                             " was provided: please provide a dataframe as argument")
                    return
                df = self.df.copy()
            ds2 = self.new_(df, db, quiet=True, nbload_libs=False)
            ds2.db = self.db
            ds2.x = self.x
            ds2.y = self.y
            ds2.chart_obj = self.chart_obj
            ds2.chart_opts = self.chart_opts
            ds2.chart_style = self.chart_style
            ds2.label = self.label
            ds2.reports = self.reports
            ds2.report_engines = self.report_engines
            ds2.backup_df = self.backup_df
            ds2.autoprint = self.autoprint
            ds2.errors_handling = self.errors_handling
            ds2.datapath = self.datapath
            ds2.report_path = self.report_path
            ds2.static_path = self.static_path
            ds2.quiet = self.quiet
        except Exception as e:
            self.err(e, "Can not duplicate instance")
            return
        if quiet is False:
            self.ok("A duplicated instance was created")
        return ds2

    def clone_(self, quiet=False):
        """
        Clone the DataSwim instance
        """
        ds2 = self._duplicate_(quiet=True)
        if ds2 is None:
            self.err("Can not clone instance")
        else:
            if quiet is False:
                self.ok("Instance cloned")
        return ds2
