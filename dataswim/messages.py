import datetime
import dateutil.relativedelta
from IPython.display import display, HTML
from goerr.colors import colors


class Messages():
    """
    A class to handle output
    """

    def ok(self, *msg):
        """
        Prints a message with an ok prefix
        """
        label = colors.green("OK")
        self._msg(label, *msg)

    def info(self, *msg):
        """
        Prints a message with an info prefix
        """
        label = colors.blue("INFO")
        self._msg(label, *msg)
        
    def status(self, *msg):
        """
        Prints a status message
        """
        label = colors.yellow("STATUS")
        self._msg(label, *msg)

    def warning(self, *msg):
        """
        Prints a warning
        """
        label = colors.yellow("WARNING")
        self._msg(label, *msg)

    def debug(self, *msg):
        """
        Prints a warning
        """
        label = colors.yellow("DEBUG")
        self._msg(label, *msg)

    def progress(self, *msg):
        """
        Prints a progress message
        """
        label = colors.purple("Progress")
        self._msg(label, *msg)

    def start(self, *msg):
        """
        Prints an start message
        """
        self.start_time = datetime.datetime.now()
        label = colors.purple("START")
        self._msg(label, *msg)

    def end(self, *msg):
        """
        Prints an end message with elapsed time
        """
        if self.start_time is None:
            self.err("No start time set: please use start() "
                "before using this function")
        endtime = datetime.datetime.now()
        rd = dateutil.relativedelta.relativedelta(endtime, self.start_time)
        endmsg = self._endmsg(rd)
        label = colors.purple("END")
        msg += ("in " + endmsg,)
        self._msg(label, *msg)
        self.start_time = None

    def html(self, label, *msg):
        """
        Prints html in notebook
        """
        lbl = "[" + label + "] "
        txt = lbl + " " + " ".join(list(msg))
        if self.notebook is True:
            html = HTML(txt)
            display(lbl + html)
        else:
            print(lbl + txt)

    def msg_(self, label, *msg):
        """
        Returns a message with a label
        """
        txt = self._unpack_msg(*msg)
        return "[" + label + "] " + txt

    def _msg(self, label, *msg):
        """
        Prints a message with a label
        """
        if self.quiet is False:
            txt = self._unpack_msg(*msg)
            print("[" + label + "] " + txt)

    def _unpack_msg(self, *msg):
        """
        Convert all message elements to string
        """
        l = []
        for m in msg:
            l.append(str(m))
        return " ".join(l)

    def _endmsg(self, rd):
        """
        Returns an end message with elapsed time
        """
        msg = ""
        s = ""
        if rd.hours > 0:
            if rd.hours > 1:
                s = "s"
            msg += colors.bold(str(rd.hours)) + " hour" + s + " "
        s = ""
        if rd.minutes > 0:
            if rd.minutes > 1:
                s = "s"
            msg += colors.bold(str(rd.minutes)) + " minute" + s + " "
        # if rd.seconds > 0:
        #    msg+=str(rd.seconds)
        # else:
        #    msg+="0."
        milliseconds = int(rd.microseconds / 1000)
        if milliseconds > 0:
            msg += colors.bold(str(rd.seconds) + "." + str(milliseconds))
        msg += " seconds"
        return msg
