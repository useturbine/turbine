import { QueryClient } from "react-query";
import axios from "axios";
import { turbineAdminApiKey, turbineApiUrl } from "./config";
import { PipelineFromAPI } from "./utils";

export const queryClient = new QueryClient();

// Fetch user's API key
export const fetchUserApiKey = async ({
  externalUserId,
}: {
  externalUserId: string;
}): Promise<string> => {
  const result = await axios.get(`${turbineApiUrl}/users/${externalUserId}`, {
    headers: {
      "X-Turbine-Key": turbineAdminApiKey,
    },
  });
  return result.data.api_key;
};

// Fetch pipelines
export const fetchPipelines = async ({
  userApiKey,
}: {
  userApiKey?: string;
}): Promise<PipelineFromAPI[]> => {
  if (!userApiKey) throw new Error("User API key is required");

  const result = await axios.get(`${turbineApiUrl}/pipelines`, {
    headers: { "X-Turbine-Key": userApiKey },
  });
  return result.data;
};

// Fetch tasks
export const fetchTasks = async ({
  userApiKey,
  pipelineId,
}: {
  userApiKey: string;
  pipelineId?: string;
}): Promise<
  {
    id: string;
    successful: boolean;
    created_at: string;
    finished_at?: string;
  }[]
> => {
  const result = await axios.get(`${turbineApiUrl}/tasks`, {
    params: { pipeline: pipelineId },
    headers: { "X-Turbine-Key": userApiKey },
  });
  return result.data;
};
