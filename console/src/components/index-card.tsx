import { Card, CardBody, Chip } from "@nextui-org/react";
import { IndexFromAPI } from "../utils";
import { useNavigate } from "react-router-dom";

export const IndexCard = ({ index }: { index: IndexFromAPI }) => {
  const navigate = useNavigate();

  const embeddingModelChipContents = {
    openai: "OpenAI",
    huggingface: "HuggingFace",
  };
  const vectorDatabaseChipContents = {
    pinecone: "Pinecone",
    milvus: "Milvus",
    weaviate: "Weaviate",
  };

  return (
    <Card isPressable onPress={() => navigate("/indexes/" + index.id)}>
      <CardBody>
        <div className="flex justify-between">
          <div className="flex gap-2 items-center">
            <h1 className="text-xl font-bold">{index.name}</h1>
            <Chip className="font-mono" size="sm">
              {embeddingModelChipContents[index.embedding_model.type]}
            </Chip>
            <Chip className="font-mono" size="sm">
              {vectorDatabaseChipContents[index.vector_database.type]}
            </Chip>
          </div>
          <span className="font-mono">{index.id}</span>
        </div>
      </CardBody>
    </Card>
  );
};
