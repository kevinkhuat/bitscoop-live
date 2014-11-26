class TastydataError(Exception):
    """A base exception for other tastydata-related errors."""
    pass


class BadRequest(TastydataError):
    """
    A generalized exception for indicating incorrect request parameters.

    Handled specially in that the message tossed by this exception will be
    presented to the end user.
    """
    pass


class InvalidFilterError(BadRequest):
    """
    Raised when the end user attempts to use a filter that has not be
    explicitly allowed.
    """
    pass
