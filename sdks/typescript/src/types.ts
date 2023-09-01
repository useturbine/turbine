type PostgresDataSource = {
  type: "postgres";
  config: {
    host: string;
    port: number;
    database: string;
    user: string;
    password: string;
    table: string;
  };
};

type MongoDataSource = {
  type: "mongo";
  config: {
    url: string;
    collection: string;
  };
};

export type ProjectConfig = {
  dataSource: PostgresDataSource | MongoDataSource;
  embeddingModel: "openai";
  vectorDB: "milvus" | "pinecone";
  similarityMetric: "cosine" | "euclidean";
};
