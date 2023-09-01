from turbine_sdk.api import BaseSDK, BaseHTTPMethods


class SearchAPI(BaseSDK, BaseHTTPMethods):
    def search(self, query):
        endpoint = "/search"
        return self._make_request(self.GET, endpoint, data={"q": query})
