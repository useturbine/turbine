import { QueryClient } from "react-query";
import axios from "axios";
import { turbineAdminApiKey, turbineApiUrl } from "./config";
import { IndexFromAPI, DataSourceFromAPI, TaskFromAPI } from "./utils";

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

// Fetch data sources
export const fetchDataSources = async ({
  userApiKey,
  indexId,
}: {
  userApiKey?: string;
  indexId?: string;
}): Promise<DataSourceFromAPI[]> => {
  if (!userApiKey) throw new Error("User API key is required");

  const result = await axios.get(`${turbineApiUrl}/data-sources`, {
    headers: { "X-Turbine-Key": userApiKey },
    params: { index_id: indexId },
  });
  return result.data;
};

// Fetch tasks
export const fetchTasks = async ({
  userApiKey,
  dataSourceId,
  indexId,
}: {
  userApiKey?: string;
  dataSourceId?: string;
  indexId?: string;
}): Promise<TaskFromAPI[]> => {
  if (!userApiKey) throw new Error("User API key is required");

  const result = await axios.get(`${turbineApiUrl}/tasks`, {
    params: { data_source_id: dataSourceId, index_id: indexId },
    headers: { "X-Turbine-Key": userApiKey },
  });
  return result.data;
};

// Fetch indexes
export const fetchIndexes = async ({
  userApiKey,
}: {
  userApiKey?: string;
}): Promise<IndexFromAPI[]> => {
  if (!userApiKey) throw new Error("User API key is required");

  const result = await axios.get(`${turbineApiUrl}/indexes`, {
    headers: { "X-Turbine-Key": userApiKey },
  });
  return result.data;
};
