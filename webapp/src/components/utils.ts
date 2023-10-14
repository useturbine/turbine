import axios from "axios";
import { turbineApiUrl } from "../config";
import { Pipeline } from "./types";

// Mutation to create pipeline
export const createPipeline = async ({
  pipeline,
  userApiKey,
}: {
  pipeline: Pipeline;
  userApiKey?: string;
}) => {
  if (!userApiKey) throw new Error("User API key is required");

  const vectorDatabaseOptions = {
    pinecone: {
      api_key: pipeline.pineconeConfig?.apiKey,
      environment: pipeline.pineconeConfig?.environment,
      index_name: pipeline.pineconeConfig?.indexName,
    },
    milvus: {
      url: pipeline.milvusConfig?.url,
      token: pipeline.milvusConfig?.token,
      collection_name: pipeline.milvusConfig?.collectionName,
    },
  };
  const vectorDatabase = vectorDatabaseOptions[pipeline.vectorDatabaseType];

  const embeddingModelOptions = {
    openai: {
      model: pipeline.openaiConfig?.model,
      api_key: pipeline.openaiConfig?.apiKey,
    },
    huggingface: {
      model: pipeline.huggingfaceConfig?.model,
      token: pipeline.huggingfaceConfig?.token,
    },
  };
  const embeddingModel = embeddingModelOptions[pipeline.embeddingModelType];

  const dataSourceOptions = {
    s3_text: {
      url: pipeline.s3TextConfig?.url,
      splitter: {
        type: "recursive",
        size: pipeline.s3TextConfig?.chunkSize,
        overlap: pipeline.s3TextConfig?.chunkOverlap,
      },
    },
  };
  const dataSource = dataSourceOptions[pipeline.dataSourceType];

  const payload = {
    name: pipeline.name,
    vector_database: {
      type: pipeline.vectorDatabaseType,
      ...vectorDatabase,
    },
    embedding_model: {
      type: pipeline.embeddingModelType,
      ...embeddingModel,
    },
    data_source: {
      type: pipeline.dataSourceType,
      ...dataSource,
    },
  };

  const result = await axios.post(`${turbineApiUrl}/pipelines`, payload, {
    headers: {
      "X-Turbine-Key": userApiKey,
    },
  });
  return result.data.id;
};

// Mutation to run pipeline
export const runPipeline = async ({
  pipelineId,
  userApiKey,
}: {
  pipelineId: string;
  userApiKey?: string;
}): Promise<string> => {
  if (!userApiKey) throw new Error("User API key is required");

  const result = await axios.post(
    `${turbineApiUrl}/pipelines/${pipelineId}/run`,
    null,
    {
      headers: {
        "X-Turbine-Key": userApiKey,
      },
    }
  );
  return result.data.id;
};

export const deletePipeline = async ({
  pipelineId,
  userApiKey,
}: {
  pipelineId: string;
  userApiKey?: string;
}) => {
  if (!userApiKey) throw new Error("User API key is required");

  await axios.delete(`${turbineApiUrl}/pipelines/${pipelineId}`, {
    headers: {
      "X-Turbine-Key": userApiKey,
    },
  });
};
