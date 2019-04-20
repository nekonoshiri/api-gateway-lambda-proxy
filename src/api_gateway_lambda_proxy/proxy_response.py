"""Data classes for response of AWS Lambda proxy integration."""

from __future__ import annotations

import dataclasses
import json
from dataclasses import field
from typing import Any, Dict, List, Optional

RawProxyResponse = Dict[str, Any]


@dataclasses.dataclass()
class BaseProxyResponse:
    """Base Proxy response."""

    statusCode: int
    body: Any = None
    headers: Dict[str, str] = field(default_factory=dict)
    multiValueHeaders: Dict[str, List[str]] = field(default_factory=dict)
    isBase64Encoded: bool = False

    def _body_encoder(self, body: Optional[str]) -> Optional[str]:
        return body

    def to_raw(self) -> RawProxyResponse:
        """Convert to RawProxyResponse."""
        result = {
            'statusCode': self.statusCode,
            'headers': self.headers,
            'multiValueHeaders': self.multiValueHeaders,
            'isBase64Encoded': self.isBase64Encoded
        }
        body_str = self._body_encoder(self.body)
        if body_str is not None:
            result['body'] = body_str
        return result


@dataclasses.dataclass()
class JsonProxyResponse(BaseProxyResponse):
    """Proxy response whose body is JSON."""

    headers: Dict[str, str] = \
        field(default_factory=lambda: {'Content-Type': 'application/json'})

    def _body_encoder(self, body: Any) -> Optional[str]:
        return None if body is None else json.dumps(body)
