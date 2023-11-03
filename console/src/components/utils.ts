import axios from "axios";
import { turbineApiUrl } from "../config";
import { DataSource, Index } from "./types";

// Mutation to create data source
export const createDataSource = async ({
  indexId,
  dataSource,
  userApiKey,
}: {
  indexId?: string;
  dataSource: DataSource;
  userApiKey?: string;
}): Promise<string> => {
  if (!userApiKey || !indexId)
    throw new Error("User API key and Index ID is required");

  const dataSourceOptions = {
    s3: {
      url: dataSource.s3Config?.url,
      splitter: {
        type: "recursive",
        size: dataSource.s3Config?.chunkSize,
        overlap: dataSource.s3Config?.chunkOverlap,
      },
    },
  };
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-expect-error
  const dataSourceConfig = dataSourceOptions[dataSource.dataSourceType];

  const payload = {
    name: dataSource.name,
    index_id: indexId,
    data_source: {
      type: dataSource.dataSourceType,
      ...dataSourceConfig,
    },
  };

  const result = await axios.post(`${turbineApiUrl}/data-sources`, payload, {
    headers: {
      "X-Turbine-Key": userApiKey,
    },
  });
  return result.data.id;
};

// Mutation to sync data source
export const syncDataSource = async ({
  dataSourceId,
  userApiKey,
}: {
  dataSourceId: string;
  userApiKey?: string;
}): Promise<string> => {
  if (!userApiKey) throw new Error("User API key is required");

  const result = await axios.post(
    `${turbineApiUrl}/data-sources/${dataSourceId}/run`,
    null,
    {
      headers: {
        "X-Turbine-Key": userApiKey,
      },
    }
  );
  return result.data.id;
};

export const createIndex = async ({
  index,
  userApiKey,
}: {
  index: Index;
  userApiKey?: string;
}): Promise<string> => {
  if (!userApiKey) throw new Error("User API key is required");

  const vectorDatabaseOptions = {
    pinecone: {
      api_key: index.pineconeConfig?.apiKey,
      environment: index.pineconeConfig?.environment,
      index_name: index.pineconeConfig?.indexName,
    },
    milvus: {
      url: index.milvusConfig?.url,
      token: index.milvusConfig?.token,
      collection_name: index.milvusConfig?.collectionName,
    },
  };
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-expect-error
  const vectorDatabase = vectorDatabaseOptions[index.vectorDatabaseType];

  const embeddingModelOptions = {
    openai: {
      model: index.openaiConfig?.model,
      api_key: index.openaiConfig?.apiKey,
    },
    huggingface: {
      model: index.huggingfaceConfig?.model,
      token: index.huggingfaceConfig?.token,
    },
  };
  const embeddingModel = embeddingModelOptions[index.embeddingModelType];

  const payload = {
    name: index.name,
    vector_database: {
      type: index.vectorDatabaseType,
      ...vectorDatabase,
    },
    embedding_model: {
      type: index.embeddingModelType,
      ...embeddingModel,
    },
  };

  const result = await axios.post(`${turbineApiUrl}/indexes`, payload, {
    headers: {
      "X-Turbine-Key": userApiKey,
    },
  });
  return result.data.id;
};

export const deleteDataSource = async ({
  dataSourceId,
  userApiKey,
}: {
  dataSourceId: string;
  userApiKey?: string;
}) => {
  if (!userApiKey) throw new Error("User API key is required");

  await axios.delete(`${turbineApiUrl}/data-sources/${dataSourceId}`, {
    headers: {
      "X-Turbine-Key": userApiKey,
    },
  });
};

export const deleteIndex = async ({
  indexId,
  userApiKey,
}: {
  indexId: string;
  userApiKey?: string;
}) => {
  if (!userApiKey) throw new Error("User API key is required");

  await axios.delete(`${turbineApiUrl}/indexes/${indexId}`, {
    headers: {
      "X-Turbine-Key": userApiKey,
    },
  });
};

export const uploadFiles = async ({
  indexId,
  files,
  userApiKey,
}: {
  indexId: string;
  files: File[];
  userApiKey?: string;
}) => {
  if (!userApiKey) throw new Error("User API key is required");

  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));

  await axios.post(`${turbineApiUrl}/indexes/${indexId}/upload`, formData, {
    headers: {
      "X-Turbine-Key": userApiKey,
    },
  });
};
