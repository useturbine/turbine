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

type S3Text = {
  url: string;
  chunkSize: number;
  chunkOverlap: number;
};

export type Pipeline = {
  name: string;

  // Data source
  dataSourceType: "s3_text";
  s3TextConfig?: S3Text;

  // Embedding model
  embeddingModelType: "huggingface" | "openai";
  openaiConfig?: OpenAI;
  huggingfaceConfig?: HuggingFace;

  // Vector database
  vectorDatabaseType: "milvus" | "pinecone";
  milvusConfig?: Milvus;
  pineconeConfig?: Pinecone;
};
