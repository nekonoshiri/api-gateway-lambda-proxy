"""Module for exceptions."""


class ProxyLambdaException(Exception):
    """Base exception for ProxyLambdaHandler."""

    pass


class ResourceNotFound(ProxyLambdaException):
    """Raised when the handler corresponded to the resource is not defined."""

    def __init__(self, resource: str) -> None:
        """Constructor."""
        self.resource = resource


class MethodNotFound(ProxyLambdaException):
    """Raised when the method of the specified resource is not defined."""

    def __init__(self, resource: str, httpMethod: str) -> None:
        """Constructor."""
        self.resource = resource
        self.httpMethod = httpMethod
