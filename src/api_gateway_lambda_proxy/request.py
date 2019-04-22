"""Data classes for request of AWS Lambda proxy integration."""

from __future__ import annotations

import dataclasses
import json
from typing import Any, Dict, List, Optional

LambdaEvent = Dict[str, Any]

LambdaContext = Any


class ProxyRequestBody:
    """Data class for body of proxy request."""

    def __init__(self, body: str):
        """Constructor."""
        self._body = body

    def get(self) -> str:
        """Get body as string."""
        return self._body

    def load_as_json(self) -> Dict[str, Any]:
        """Parse body as JSON and return dictionary."""
        return json.loads(self._body)


@dataclasses.dataclass(frozen=True)
class ProxyRequest:
    """Data class for proxy request."""

    resource: str
    path: str
    httpMethod: str
    headers: Dict[str, str]
    multiValueHeaders: Dict[str, List[str]]
    queryStringParameters: Dict[str, str]
    multiValueQueryStringParameters: Dict[str, List[str]]
    pathParameters: Dict[str, str]
    stageVariables: Dict[str, str]
    requestContext: Dict[str, Any]
    body: Optional[ProxyRequestBody]
    isBase64Encoded: bool

    @staticmethod
    def from_event(event: LambdaEvent) -> ProxyRequest:
        """Convert event dictionary to ProxyRequst."""
        def concat(x: Optional[Dict[Any, Any]]) -> Dict[Any, Any]:
            """Convert to empty dictionary iff the argument is None."""
            return {} if x is None else x

        return ProxyRequest(
            resource=event['resource'],
            path=event['path'],
            httpMethod=event['httpMethod'],
            headers=concat(event['headers']),
            multiValueHeaders=concat(event['multiValueHeaders']),
            queryStringParameters=concat(event['queryStringParameters']),
            multiValueQueryStringParameters=concat(
                event['multiValueQueryStringParameters']
            ),
            pathParameters=concat(event['pathParameters']),
            stageVariables=concat(event['stageVariables']),
            requestContext=concat(event['requestContext']),
            body=ProxyRequestBody(event['body'])
            if event['body'] is not None else None,
            isBase64Encoded=event['isBase64Encoded']
        )
