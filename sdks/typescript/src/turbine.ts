import axios, { Axios } from "axios";
import { Project, ProjectConfig, SearchResult } from "./types";
import { snakeifyKeys, camelizeKeys } from "./utils";

export class Turbine {
  private axios: Axios;

  constructor(apiKey: string, baseUrl?: string) {
    this.axios = axios.create({
      baseURL: baseUrl ?? "https://api.useturbine.com/v1",
      headers: {
        "X-Turbine-Key": apiKey,
      },
    });
  }

  async createProject(config: ProjectConfig): Promise<string> {
    const response = await this.axios.post("/projects", snakeifyKeys(config));
    return response.data.id;
  }

  async getProject(projectId: string): Promise<Project> {
    const response = await this.axios.get(`/projects/${projectId}`);
    return camelizeKeys(response.data);
  }

  async getProjects(): Promise<Project[]> {
    const response = await this.axios.get("/projects");
    return camelizeKeys(response.data);
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
