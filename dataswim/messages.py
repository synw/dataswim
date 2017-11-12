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
        endmsg = self.msg_(label, *msg)
        print(endmsg)

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
        label = colors.purple("DEBUG")
        self._msg(label, *msg)

    def end(self, *msg):
        """
        Prints an end message
        """
        label = colors.purple("END")
        self._msg(label, *msg)

    def start(self, *msg):
        """
        Prints an start message
        """
        label = colors.purple("START")
        self._msg(label, *msg)

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
