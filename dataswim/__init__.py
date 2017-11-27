import pandas as pd
from .db import Db
from .charts import Plot
from .data import Df
from .report import Report
from .errors import Errors
from .messages import Messages

__version__ = "0.3.7"


class DataSwim(Db, Df, Plot, Report, Errors, Messages):
    """
    Main class
    """

    def __init__(self, df=None, db=None):
        """
        Initialize with an empty dataframe
        """
        global __version__
        self.version = __version__
        self.df = df
        self.db = db
        self.x = None
        self.y = None
        self.chart_obj = None
        self.chart_opts = dict(width=940)
        self.chart_style = dict(color="blue")
        self.engine = "bokeh"
        self.label = None
        self.backup_df = None
        self.autoprint = True
        self.errors_handling = "exceptions"
        self.notebook = False
        self.header = self._header
        self.footer = self._footer
        self.reports = []
        self.report_engines = [self.engine]
        self.start_time = None
        self.influx_cli = None

    def __repr__(self):
        num = 0
        if self.df is not None:
            num = len(self.df.index)
        msg = "<DataSwim object | " + str(num) + " rows>"
        return msg

    def new_(self, df=None, db=None, quiet=False):
        """
        Returns a new DataSwim instance from a dataframe
        """
        try:
            ds2 = DataSwim(df, db)
        except Exception as e:
            self.err(e, self.new_, "Can not set new instance")
        if self.autoprint is True and quiet is False:
            self.ok("A new instance was created")
        return ds2

    def set_df(self, data, **args):
        """
        Set a dataframe and an instance
        """
        self.df = pd.DataFrame(data, **args)


ds = DataSwim()
