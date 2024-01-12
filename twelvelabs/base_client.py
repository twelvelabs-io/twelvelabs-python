import httpx
from .constants import DEFAULT_TIMEOUT, API_KEY_HEADER
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
        try:
            response = self._client.request(method, url, **kwargs)
            response.raise_for_status()
            if "application/json" in response.headers.get("Content-Type", ""):
                return response.json()
            return response.text
        except httpx.HTTPError as e:
            return {"error": str(e)}

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        return self._request("GET", url, params=params, **kwargs)

    def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
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
