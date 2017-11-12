from goerr.colors import colors


class Messages():
    """
    A class to handle output
    """

    def ok(self, *msg):
        """
        Prints a message with an ok prefix
        """
        print("[" + colors.green("OK") + "] " + " ".join(msg))

    def info(self, *msg):
        """
        Prints a message with an info prefix
        """
        print("[" + colors.blue("INFO") + "] " + " ".join(msg))

    def warning(self, *msg):
        """
        Prints a warning
        """
        print("[" + colors.yellow("WARNING") + "] " + " ".join(msg))

    def debug(self, *msg):
        """
        Prints a warning
        """
        print("[" + colors.purple("DEBUG") + "] " + " ".join(msg))
