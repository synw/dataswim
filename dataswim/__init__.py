from .messages import Message
from .db import Db
from .charts import Plot
from .maps import Map
from .data import Df
from .report import Report
from .base import DsBase

__version__ = "0.5.1"


class Ds(Db, Df, Plot, Map, Report, DsBase):
    """
    Main class
    """

    def __init__(self, df=None, db=None, nbload_libs=True):
        """
        Initialize with an empty dataframe
        """
        self.msg = Message()
        self.version = __version__
        self.df = df
        self.db = db
        self.x = None
        self.y = None
        self.chart_obj = None
        self.chart_opts = dict(width=880)
        self.chart_style = {}
        self.engine = "bokeh"
        self.label = None
        self.backup_df = None
        self.autoprint = False
        self.errors_handling = "exceptions"
        self.notebook = False
        # self.header = self._header
        # self.footer = self._footer
        self.reports = []
        self.report_engines = []
        self.start_time = None
        self.influx_cli = None
        self.datapath = None
        self.report_path = None
        self.static_path = None
        self.quiet = False
        # self.nan = nan
        self.color_index = 0
        self.dsmap = None
        self.altair_encode = {}

        if self._isnotebook() is True and nbload_libs is True:
            self.notebook = True
            import holoviews as hv
            hv.extension("bokeh")
            try:
                import altair as alt
                alt.renderers.enable('notebook')
            except Exception:
                pass

    def __repr__(self):
        num = 0
        if self.df is not None:
            num = len(self.df.index)
        msg = "<DataSwim object | " + str(num) + " rows>"
        if self.notebook is True:
            self.df.head()
            return str(self.df.head(5))
        return msg

    def _isnotebook(self):
        try:
            shell = get_ipython().__class__.__name__
            if shell == 'ZMQInteractiveShell':
                return True
            else:
                return False
        except NameError:
            return False
