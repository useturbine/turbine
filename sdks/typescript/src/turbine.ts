import axios, { Axios } from "axios";
import { ProjectConfig } from "./types";
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

  async createProject(project: ProjectConfig) {
    return await this.axios.post("/projects", snakeifyKeys(project));
  }

  async getProject(projectId: string) {
    return await this.axios.get(`/projects/${projectId}`);
  }

  async deleteProject(projectId: string) {
    return await this.axios.delete(`/projects/${projectId}`);
  }

  async search(projectId: string, query: string, limit: number = 10) {
    return await this.axios.get(`/projects/${projectId}/search`, {
      params: {
        query,
        limit,
      },
    });
  }
}
