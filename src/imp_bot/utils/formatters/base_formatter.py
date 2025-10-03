from abc import ABC

class BaseFormatter(ABC):
    """
    Parent Formatter Class
    """

    def __init__(self, arg):
        self.arg = arg