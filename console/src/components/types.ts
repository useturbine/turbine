type HuggingFace = {
  model: string;
  token: string;
};

type OpenAI = {
  model: string;
  apiKey: string;
};

type Milvus = {
  url: string;
  token: string;
  collectionName: string;
};

type Pinecone = {
  apiKey: string;
  environment: string;
  indexName: string;
};

type S3 = {
  url: string;
  chunkSize: number;
  chunkOverlap: number;
};

export type DataSource = {
  name: string;

  // Data source
  dataSourceType: "s3" | "postgres" | "mongo" | "notion";
  s3Config?: S3;
};

export type Index = {
  name: string;

  // Embedding model
  embeddingModelType: "huggingface" | "openai";
  openaiConfig?: OpenAI;
  huggingfaceConfig?: HuggingFace;

  // Vector database
  vectorDatabaseType: "milvus" | "pinecone" | "weaviate" | "chroma";
  milvusConfig?: Milvus;
  pineconeConfig?: Pinecone;
};
