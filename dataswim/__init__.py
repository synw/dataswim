# @PydevCodeAnalysisIgnore
import pandas as pd
from numpy.core.numeric import nan
from .db import Db
from .charts import Plot
from .maps import Map
from .data import Df
from .report import Report
from .messages import Messages
from .errors import Error

version = "0.4.24"


class DataSwim(Db, Df, Plot, Map, Report, Messages, Error):
    """
    Main class
    """

    def __init__(self, df=None, db=None):
        """
        Initialize with an empty dataframe
        """
        self.msg = Messages()
        self.version = version
        self.df = df
        self.db = db
        self.x = None
        self.y = None
        self.chart_obj = None
        self.chart_opts = dict(width=940)
        self.chart_style = {}
        self.engine = "bokeh"
        self.label = None
        self.backup_df = None
        self.autoprint = False
        self.errors_handling = "exceptions"
        self.notebook = False
        self.header = self._header
        self.footer = self._footer
        self.reports = []
        self.report_engines = []
        self.start_time = None
        self.influx_cli = None
        self.datapath = None
        self.report_path = None
        self.static_path = None
        self.quiet = False
        self.nan = nan
        self.color_index = 0
        self.dsmap = None
        self.altair_encode = {}

    def __repr__(self):
        num = 0
        if self.df is not None:
            num = len(self.df.index)
        msg = "<DataSwim object | " + str(num) + " rows>"
        return msg

    def new_(self, df=pd.DataFrame(), db=None, quiet=False):
        """
        Returns a new DataSwim instance from a dataframe
        """
        ds2 = DataSwim(df, db)
        if quiet is False:
            self.ok("A new instance was created")
        return ds2


ds = DataSwim()
