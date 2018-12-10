from goerr import Err


class Error():
    """
    A class to manage errors
    """
    
    def err(self, *args):
        """
        Handle an error
        """
        Err().new(*args)
