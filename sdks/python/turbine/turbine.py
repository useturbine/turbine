from typing import Optional, List
from httpx import Client
from .types import Project, SearchResult, ProjectConfig


class Turbine:
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.client = Client(
            headers={"X-Turbine-Key": api_key},
            base_url=base_url or "https://api.useturbine.com/v1",
        )

    def get_projects(self) -> List[Project]:
        response = self.client.get("/projects")
        if response.status_code != 200:
            raise Exception(response.text)
        return [Project(**project) for project in response.json()]

    def get_project(self, project_id: str) -> Project:
        response = self.client.get(f"/projects/{project_id}")
        if response.status_code != 200:
            raise Exception(response.text)
        return Project(**response.json())

    def create_project(self, config: ProjectConfig) -> str:
        response = self.client.post("/projects", json=config.model_dump())
        if response.status_code != 201:
            raise Exception(response.text)
        return response.json()["id"]

    def search(
        self, project_id: str, query: str, limit: int = 10
    ) -> List[SearchResult]:
        response = self.client.get(
            f"/projects/{project_id}/search", params={query, limit}
        )
        if response.status_code != 200:
            raise Exception(response.text)
        return [SearchResult(**result) for result in response.json()]
