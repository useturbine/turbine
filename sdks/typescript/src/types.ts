export type PostgresDataSource = {
  type: "postgres";
  config: {
    url: string;
    table: string;
  };
  fields: string[];
};

export type MongoDataSource = {
  type: "mongo";
  config: {
    url: string;
    collection: string;
  };
  fields: string[];
};

export type ProjectConfig = {
  dataSource: PostgresDataSource | MongoDataSource;
  embeddingModel: "text-embedding-ada-002" | "all-MiniLM-L6-v2";
  vectorDb: "milvus" | "pinecone";
};

export type Project = {
  id: string;
  config: ProjectConfig;
};

export type SearchResult = {
  id: string;
  score: number;
};
