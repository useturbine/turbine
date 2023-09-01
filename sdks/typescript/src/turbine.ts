import axios, { Axios } from "axios";
import { Project, ProjectConfig, SearchResult } from "./types";
import { snakeifyKeys } from "./utils";

export class Turbine {
  private axios: Axios;

  constructor(apiKey: string) {
    this.axios = axios.create({
      baseURL: "http://localhost/v1",
      headers: {
        "X-Turbine-Key": apiKey,
      },
    });
  }

  async createProject(project: ProjectConfig): Promise<string> {
    const response = await this.axios.post("/projects", snakeifyKeys(project));
    return response.data.id;
  }

  async getProject(projectId: string): Promise<Project> {
    const response = await this.axios.get(`/projects/${projectId}`);
    return response.data;
  }

  async getProjects(): Promise<Project[]> {
    const response = await this.axios.get("/projects");
    return response.data;
  }

  async deleteProject(projectId: string): Promise<void> {
    await this.axios.delete(`/projects/${projectId}`);
  }

  async search(
    projectId: string,
    query: string,
    limit: number = 10
  ): Promise<SearchResult[]> {
    const response = await this.axios.get(`/projects/${projectId}/search`, {
      params: {
        query,
        limit,
      },
    });
    return response.data;
  }
}
