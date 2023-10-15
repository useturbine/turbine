import { Card } from "flowbite-react";
import { PipelineFromAPI } from "../utils";

export const PipelineCard = ({ pipeline }: { pipeline: PipelineFromAPI }) => {
  const dataSourceDescriptions = {
    s3_text: "text files from S3 bucket",
  };
  const embeddingModelDescriptions = {
    openai: "OpenAI",
    huggingface: "Hugging Face",
  };
  const vectorDatabaseDescriptions = {
    milvus: "Milvus",
    pinecone: "Pinecone",
  };
  const dataSourceDescription =
    dataSourceDescriptions[pipeline.data_source.type];
  const embeddingModelDescription =
    embeddingModelDescriptions[pipeline.embedding_model.type];
  const vectorDatabaseDescription =
    vectorDatabaseDescriptions[pipeline.vector_database.type];

  return (
    <Card href={`/pipelines/${pipeline.id}`}>
      <div className="flex flex-col gap-1">
        <h1 className="text-xl font-bold">{pipeline.name}</h1>
        <span className="font-mono">{pipeline.id}</span>
        <p className="text-gray-500 dark:text-gray-400">
          Uses <span className="font-bold">{dataSourceDescription}</span> as
          data source,{" "}
          <span className="font-bold">{embeddingModelDescription}</span> as
          embedding model, and{" "}
          <span className="font-bold">{vectorDatabaseDescription}</span> as
          vector database.
        </p>
      </div>
    </Card>
  );
};
