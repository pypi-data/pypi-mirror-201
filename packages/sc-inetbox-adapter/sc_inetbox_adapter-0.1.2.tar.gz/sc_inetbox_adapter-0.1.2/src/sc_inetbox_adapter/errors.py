"""Errors for the Swisscom Internetbox"""

class SwisscomInetboxException(Exception):
    """General Swisscom Internetbox Exception"""

class NoActiveSessionException(SwisscomInetboxException):
    """No authorized session available"""
