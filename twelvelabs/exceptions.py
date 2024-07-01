from __future__ import annotations

import httpx

from typing import Optional, Literal

__all__ = [
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
]


class TwelveLabsError(Exception):
    pass


class APIError(TwelveLabsError):
    message: str
    request: httpx
    body: Optional[object]

    def __init__(
        self, message: str, request: httpx.Request, *, body: Optional[object]
    ) -> None:
        super().__init__(message)
        self.message = message
        self.request = request
        self.body = body


class APIStatusError(APIError):
    """Raised API response return a status code of 4xx or 5xx."""

    response: httpx.Response
    status_code: int

    def __init__(
        self, message: str, *, response: httpx.Response, body: Optional[object]
    ) -> None:
        super().__init__(message, response.request, body=body)
        self.response = response
        self.status_code = response.status_code


class APIConnectionError(APIError):
    def __init__(
        self, *, message: str = "Failed connection", request: httpx.Request
    ) -> None:
        super().__init__(message, request, body=None)


class APITimeoutError(APIConnectionError):
    def __init__(self, *, request: httpx.Request) -> None:
        super().__init__(message="Request timed out", request=request)


class BadRequestError(APIStatusError):
    status_code: Literal[400] = 400


class AuthenticationError(APIStatusError):
    status_code: Literal[401] = 401


class PermissionDeniedError(APIStatusError):
    status_code: Literal[403] = 403


class NotFoundError(APIStatusError):
    status_code: Literal[404] = 404


class ConflictError(APIStatusError):
    status_code: Literal[409] = 409


class UnprocessableEntityError(APIStatusError):
    status_code: Literal[422] = 422


class RateLimitError(APIStatusError):
    status_code: Literal[429] = 429


class InternalServerError(APIStatusError):
    pass
