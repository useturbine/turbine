import { useOutletContext } from "react-router-dom";

type ContextType = { userApiKey?: string; externalUserId?: string };

export function useRootContext() {
  return useOutletContext<ContextType>();
}

type OpenAIModel = {
  type: "openai";
  api_key: string;
  model: string;
};

type HuggingFaceModel = {
  type: "huggingface";
  model: string;
  token: string;
};

type EmbeddingModel = OpenAIModel | HuggingFaceModel;

type MilvusVectorDatabase = {
  type: "milvus";
  url: string;
  token: string;
  collection_name: string;
};

type PineconeVectorDatabase = {
  type: "pinecone";
  api_key: string;
  environment: string;
  index_name: string;
};

type VectorDatabase = MilvusVectorDatabase | PineconeVectorDatabase;

type S3TextDataSource = {
  type: "s3_text";
  url: string;
  splitter: {
    size: number;
    overlap: number;
  };
};

export type PipelineFromAPI = {
  id: string;
  name: string;
  embedding_model: EmbeddingModel;
  vector_database: VectorDatabase;
  data_source: S3TextDataSource;
};

export type TaskFromAPI = {
  id: string;
  created_at: string;
  finished_at?: string;
  successful: boolean;
  pipeline: string;
};
