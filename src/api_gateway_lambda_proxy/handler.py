"""Main module defining ProxyLambdaHandler class."""

import logging
from typing import Any, Callable, Dict, Optional, Tuple, Union

from api_gateway_lambda_proxy.exception import (
    MethodNotFound, ResourceNotFound
)
from api_gateway_lambda_proxy.request import (
    LambdaContext, LambdaEvent, ProxyRequest
)
from api_gateway_lambda_proxy.response import (
    BaseProxyResponse, JsonProxyResponse, RawProxyResponse
)

ProxyRequestHandler = Callable[
    [ProxyRequest, LambdaContext], BaseProxyResponse
]
ProxyErrorHandler = Callable[[Exception], BaseProxyResponse]
ProxyPrePreHandler = Callable[
    [LambdaEvent, Any], Optional[Tuple[LambdaEvent, Any]]
]
ProxyPreHandler = Callable[[ProxyRequest], Optional[ProxyRequest]]
ProxyPostHandler = Callable[[BaseProxyResponse], Optional[BaseProxyResponse]]
ProxyPostPostHandler = Callable[[RawProxyResponse], Optional[RawProxyResponse]]

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
            pre_pre_result = self._pre_pre_handler(event, context)
            if pre_pre_result is not None:
                (event, context) = pre_pre_result

            request = ProxyRequest.from_event(event)
            pre_result = self._pre_handler(request)
            if pre_result is not None:
                request = pre_result

            if request.resource not in self._routes:
                raise ResourceNotFound(request.resource)
            if request.httpMethod not in self._routes[request.resource]:
                raise MethodNotFound(request.resource, request.httpMethod)

            handler = self._routes[request.resource][request.httpMethod]
            response = handler(request, context)

            post_result = self._post_handler(response)
            if post_result is not None:
                response = post_result

            raw_response = response.to_raw()
            post_post_result = self._post_post_handler(raw_response)
            if post_post_result is not None:
                raw_response = post_post_result

            return raw_response
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
    ) -> None:
        pass

    def _default_pre_handler(self, request: ProxyRequest) -> None:
        pass

    def _default_post_handler(self, response: BaseProxyResponse) -> None:
        pass

    def _default_post_post_handler(
        self, raw_response: RawProxyResponse
    ) -> None:
        pass
