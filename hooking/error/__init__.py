"""Exceptions"""


class Error(Exception):
    """Error class"""
    pass


class ChainBreak(Error):
    """Break the execution of a chain of hooks"""
    pass
