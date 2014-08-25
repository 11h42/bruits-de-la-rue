# Api error code : XYYZZ
# X API version
# YY Model attached
# ZZ error number

error_codes = {
    #global
    "10900": "the json sent is not a valid json",
    "10901": "your contacts' limit is reached",
    "10666": "unknown error"
}


class BadParameterError(Exception):
    """
    Bad parameter exception
    """

    def __init__(self, parameter):
        self.code = 10410
        self.message = error_codes['10410'] % parameter