from turbine_sdk.turbine.config import BASE_URL, HEADERS
from turbine_sdk.exceptions.exceptions import APIRequestException

import requests
import httpx


class BaseHTTPMethods:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class BaseSDK:
    def __init__(self, token=None):
        self.token = token
        self.headers = {**HEADERS, "Authorization": f"Bearer {self.token}"}

    def _make_request(self, method, endpoint, data=None):
        url = f"{BASE_URL}{endpoint}"

        resp = requests.request(method, url, headers=self.headers, data=data)
        if resp.status_code >= 400:
            raise APIRequestException(resp.status_code, endpoint, resp.text)

        return resp.json()


class AsyncBaseSDK:
    def __init__(self, token):
        self.token = token
        self.headers = {**HEADERS, "Authorization": f"Bearer {self.token}"}

    async def _async_make_request(self, method, endpoint, data=None):
        async with httpx.AsyncClient() as client:
            url = f"{BASE_URL}{endpoint}"
            resp = await client.request(method, url, headers=self.headers, json=data)

            if resp.status_code >= 400:
                raise APIRequestException(resp.status_code, endpoint, resp.text)

            return resp.json()
