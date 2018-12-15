

class DbBase():
    """
    A base class for database management
    """

    def _check_db(self) -> bool:
        if self.db is None:
            self.warning("Database not connected")
            return False
        return True
