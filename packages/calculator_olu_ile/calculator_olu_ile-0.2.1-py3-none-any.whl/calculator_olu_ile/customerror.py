"""exception class to identify none numeric errors"""


class NoneNumericValueError(Exception):
    def __init__(self, value):
        """message displayed to user in cases where a none numeric was entered"""
        self.message = "A non-numeric value %s was used as input" % str(value)
        super().__init__(self.message)
