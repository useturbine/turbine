from turbine_sdk.api import BaseSDK, BaseHTTPMethods, AsyncBaseSDK


class ProjectAPI(BaseSDK, BaseHTTPMethods, AsyncBaseSDK):
    def __init__(self, token):
        super().__init__(token)

    def get_project(self, project_id=None):
        endpoint = f"/project/{project_id}" if project_id else "/project"
        return self._make_request(self.GET, endpoint)

    def create_project(self, project_data):
        endpoint = "/project"
        return self._make_request(self.POST, endpoint, project_data)

    def update_project(self, project_id, project_data):
        endpoint = f"/project/{project_id}"
        return self._make_request(self.PUT, endpoint, project_data)

    def delete_project(self, project_id):
        endpoint = f"/project/{project_id}"
        return self._make_request(self.DELETE, endpoint)

    async def get_project_async(self, project_id=None):
        endpoint = f"/project/{project_id}" if project_id else "/project"
        return await self._make_request(self.GET, endpoint)

    async def create_project_async(self, project_data):
        endpoint = "/project"
        return await self._make_request(self.POST, endpoint, project_data)

    async def update_project_async(self, project_id, project_data):
        endpoint = f"/project/{project_id}"
        return await self._make_request(self.PUT, endpoint, project_data)

    async def delete_project_async(self, project_id):
        endpoint = f"/project/{project_id}"
        return await self._make_request(self.DELETE, endpoint)
