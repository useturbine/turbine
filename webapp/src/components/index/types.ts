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
};

type Pinecone = {
  apiKey: string;
  environment: string;
};

export type Index = {
  name: string;
  vectorDbType: "milvus" | "pinecone";
  embeddingModelType: "huggingface" | "openai";
  milvusConfig: Milvus;
  pineconeConfig: Pinecone;
  openaiConfig: OpenAI;
  huggingfaceConfig: HuggingFace;
  embeddingDimension: number;
  similarityMetric: string;
};
