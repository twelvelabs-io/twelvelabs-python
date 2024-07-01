import httpx
import json

from . import exceptions
from .constants import DEFAULT_TIMEOUT, API_KEY_HEADER
from .exceptions import APIStatusError, APITimeoutError
from typing import Optional, Dict, Any


class APIClient:
    _client: httpx.Client

    def __init__(
        self,
        base_url: str,
        api_key: str,
        *,
        timeout: Optional[httpx.Timeout] = DEFAULT_TIMEOUT,
    ) -> None:
        httpClient = httpx.Client(
            base_url=base_url,
            headers={API_KEY_HEADER: api_key},
            timeout=timeout,
        )
        self._client = httpClient

    def _request(self, method: str, url: str, **kwargs) -> Any:
        response = None
        try:
            response = self._client.request(method, url, **kwargs)
            response.raise_for_status()
        except httpx.TimeoutException as e:
            raise APITimeoutError(request=getattr(response, "_request", None))
        except httpx.HTTPStatusError as e:
            raise self._make_status_error(e.response)
        except Exception as e:
            raise exceptions.APIConnectionError(
                request=getattr(response, "_request", None)
            )

        if len(response.content) > 0 and "application/json" in response.headers.get(
            "Content-Type", ""
        ):
            return response.json()
        return response.text

    def _request_stream(self, method: str, url: str, **kwargs):
        return self._client.stream(method, url, **kwargs)

    def _make_status_error(self, response: httpx.Response) -> APIStatusError:
        if response.is_closed and not response.is_stream_consumed:
            body = None
            err_msg = f"Error code: {response.status_code}"
        else:
            err_text = response.text.strip()
            body = err_text

            try:
                body = json.loads(err_text)
                err_msg = f"Error code: {response.status_code} - {body}"
            except Exception:
                err_msg = err_text or f"Error code: {response.status_code}"

        if response.status_code == 400:
            return exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return exceptions.PermissionDeniedError(
                err_msg, response=response, body=body
            )

        if response.status_code == 404:
            return exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return exceptions.UnprocessableEntityError(
                err_msg, response=response, body=body
            )

        if response.status_code == 429:
            return exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return self._request("GET", url, params=params, **kwargs)

    def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        *,
        stream: bool = False,
        **kwargs,
    ) -> Any:
        if stream:
            return self._request_stream("POST", url, data=data, json=json, **kwargs)
        return self._request("POST", url, data=data, json=json, **kwargs)

    def patch(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        return self._request("PATCH", url, data=data, json=json, **kwargs)

    def put(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        return self._request("PUT", url, data=data, json=json, **kwargs)

    def delete(self, url: str, **kwargs) -> Any:
        return self._request("DELETE", url, **kwargs)
