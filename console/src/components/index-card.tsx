import { Card, CardBody, Chip } from "@nextui-org/react";
import { IndexFromAPI } from "../utils";
import { useNavigate } from "react-router-dom";

export const IndexCard = ({ index }: { index: IndexFromAPI }) => {
  const navigate = useNavigate();

  return (
    <Card isPressable onPress={() => navigate("/indexes/" + index.id)}>
      <CardBody>
        <div className="flex justify-between">
          <div className="flex gap-2 items-center">
            <h1 className="text-xl font-bold">{index.name}</h1>
            <Chip className="font-mono">OpenAI</Chip>
            <Chip className="font-mono">Pinecone</Chip>
          </div>
          <span className="font-mono">{index.id}</span>
        </div>
      </CardBody>
    </Card>
  );
};
