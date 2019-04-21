"""Main module defining ProxyLambdaHandler class."""

import logging
from typing import Any, Callable, Dict, Tuple, Union

from api_gateway_lambda_proxy.exception import (
    MethodNotFound, ResourceNotFound
)
from api_gateway_lambda_proxy.proxy_request import (
    LambdaContext, LambdaEvent, ProxyRequest
)
from api_gateway_lambda_proxy.proxy_response import (
    BaseProxyResponse, JsonProxyResponse, RawProxyResponse
)

ProxyRequestHandler = Callable[
    [ProxyRequest, LambdaContext], BaseProxyResponse
]
ProxyErrorHandler = Callable[[Exception], BaseProxyResponse]
ProxyPrePreHandler = Callable[[LambdaEvent, Any], Tuple[LambdaEvent, Any]]
ProxyPreHandler = Callable[[ProxyRequest], ProxyRequest]
ProxyPostHandler = Callable[[BaseProxyResponse], BaseProxyResponse]
ProxyPostPostHandler = Callable[[RawProxyResponse], RawProxyResponse]

RequestHandlerDecorator = Callable[[ProxyRequestHandler], None]


class ProxyLambdaHandler:
    """Handler class for AWS Lambda Proxy Integration."""

    def __init__(
        self, *, log_level: Union[int, str] = logging.WARNING
    ) -> None:
        """Initialize instance variales and logger."""
        self.logger = logging.getLogger()
        self.logger.setLevel(log_level)

        self._routes: Dict[str, Dict[str, ProxyRequestHandler]] = {}
        self._error_handler: ProxyErrorHandler = self._default_error_handler
        self._pre_pre_handler: ProxyPrePreHandler = \
            self._default_pre_pre_handler
        self._pre_handler: ProxyPreHandler = self._default_pre_handler
        self._post_handler: ProxyPostHandler = self._default_post_handler
        self._post_post_handler: ProxyPostPostHandler = \
            self._default_post_post_handler

    def __call__(self, event: LambdaEvent, context: Any) -> RawProxyResponse:
        """Call as a lambda handler."""
        try:
            (event, context) = self._pre_pre_handler(event, context)
            request = self._pre_handler(ProxyRequest.from_event(event))

            if request.resource not in self._routes:
                raise ResourceNotFound(request.resource)
            if request.httpMethod not in self._routes[request.resource]:
                raise MethodNotFound(request.resource, request.httpMethod)

            handler = self._routes[request.resource][request.httpMethod]
            return self._post_post_handler(
                self._post_handler(handler(request, context)).to_raw()
            )
        except Exception as e:
            return self._error_handler(e).to_raw()

    def route(self, resource: str, httpMethod: str) -> RequestHandlerDecorator:
        """Base decorator for handler."""
        def _decorator(handler: ProxyRequestHandler) -> None:
            if resource not in self._routes:
                self._routes[resource] = {}
            self._routes[resource][httpMethod] = handler
        return _decorator

    def get(self, resource: str) -> RequestHandlerDecorator:
        """Decorator for get handler."""
        return self.route(resource, 'GET')

    def head(self, resource: str) -> RequestHandlerDecorator:
        """Decorator for head handler."""
        return self.route(resource, 'HEAD')

    def post(self, resource: str) -> RequestHandlerDecorator:
        """Decorator for post handler."""
        return self.route(resource, 'POST')

    def put(self, resource: str) -> RequestHandlerDecorator:
        """Decorator for put handler."""
        return self.route(resource, 'PUT')

    def delete(self, resource: str) -> RequestHandlerDecorator:
        """Decorator for delete handler."""
        return self.route(resource, 'DELETE')

    def patch(self, resource: str) -> RequestHandlerDecorator:
        """Decorator for patch handler."""
        return self.route(resource, 'PATCH')

    def error_handler(self, handler: ProxyErrorHandler) -> None:
        """Decorator for error handler."""
        self._error_handler = handler

    def pre_pre_handler(self, handler: ProxyPrePreHandler) -> None:
        """Decorator for pre-pre-handler."""
        self._pre_pre_handler = handler

    def pre_handler(self, handler: ProxyPreHandler) -> None:
        """Decorator for pre-handler."""
        self._pre_handler = handler

    def post_handler(self, handler: ProxyPostHandler) -> None:
        """Decorator for post-handler."""
        self._post_handler = handler

    def post_post_handler(self, handler: ProxyPostPostHandler) -> None:
        """Decorator for post-post-handler."""
        self._post_post_handler = handler

    def _default_error_handler(self, _: Exception) -> JsonProxyResponse:
        self.logger.exception('')
        return JsonProxyResponse(500, {
            'message': 'Internal server error'
        })

    def _default_pre_pre_handler(
        self, event: LambdaEvent, context: Any
    ) -> Tuple[LambdaEvent, Any]:
        return (event, context)

    def _default_pre_handler(self, request: ProxyRequest) -> ProxyRequest:
        return request

    def _default_post_handler(
        self, response: BaseProxyResponse
    ) -> BaseProxyResponse:
        return response

    def _default_post_post_handler(
        self, raw_response: RawProxyResponse
    ) -> RawProxyResponse:
        return raw_response
