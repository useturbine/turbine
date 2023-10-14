import { QueryClient } from "react-query";
import axios from "axios";
import { turbineAdminApiKey, turbineApiUrl } from "./config";

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

// Fetch indexes
export const fetchIndexes = async ({
  userApiKey,
}: {
  userApiKey?: string;
}): Promise<
  {
    id: string;
    name: string;
    embedding_model: {
      type: "openai" | "huggingface";
    };
    vector_db: {
      type: "milvus" | "pinecone";
    };
  }[]
> => {
  if (!userApiKey) throw new Error("User API key is required");

  const result = await axios.get(`${turbineApiUrl}/indexes`, {
    headers: { "X-Turbine-Key": userApiKey },
  });
  return result.data;
};

// Fetch pipelines
export const fetchPipelines = async ({
  userApiKey,
  indexId,
}: {
  userApiKey: string;
  indexId: string;
}): Promise<
  {
    id: string;
    name: string;
  }[]
> => {
  const result = await axios.get(`${turbineApiUrl}/pipelines`, {
    params: { index: indexId },
    headers: { "X-Turbine-Key": userApiKey },
  });
  return result.data;
};

// Fetch tasks
export const fetchTasks = async ({
  userApiKey,
  indexId,
}: {
  userApiKey: string;
  indexId: string;
}): Promise<
  {
    id: string;
    successful: boolean;
    created_at: string;
    finished_at?: string;
  }[]
> => {
  const result = await axios.get(`${turbineApiUrl}/tasks`, {
    params: { index: indexId },
    headers: { "X-Turbine-Key": userApiKey },
  });
  return result.data;
};
