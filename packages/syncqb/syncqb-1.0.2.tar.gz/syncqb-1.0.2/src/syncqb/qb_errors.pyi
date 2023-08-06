from lxml import etree as etree
from requests.models import Response

class QBError(Exception):
    """ Base class for all Quickbase errors"""
    message: str = ...
    response: Response | None = ...
    def __init__(self, message: str, response: Response | None = None) -> None:
        """
        :param message: (str) The error message
        :param response: (Response or None) The response object if available
        """
        ...

class QBAuthError(QBError):
    """ Raised when authentication fails """
    def __init__(self, message: str) -> None: ...

class QBConnectionError(QBError):
    """ Raised when a connection error occurs """
    def __init__(self, message: str) -> None: ...

class QBResponseError(QBError):
    """ Raised when a response error occurs """
    def __init__(self, message: str, response: Response | None = None) -> None: ...

class QuickbaseError(QBError):
    """ Raised when an error occurs but the response is ok """
    def __init__(self, message: str, response: Response | None = None) -> None: ...
