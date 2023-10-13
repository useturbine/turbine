import { useEffect, useState } from "react";
import { useRootContext } from "../utils";
import { turbineApiUrl } from "../config";
import { Accordion, Button, Card } from "flowbite-react";
import CreateIndexButton from "./create-index-button";
import { ClickToCopy } from "./click-to-copy";

export const ListIndices = () => {
  const [indices, setIndices] = useState([]);
  const { userApiKey } = useRootContext();

  // Fetch indices created by the user
  useEffect(() => {
    const fetchIndices = async () => {
      if (!userApiKey) return;

      const result = await fetch(`${turbineApiUrl}/indices`, {
        headers: {
          "X-Turbine-Key": userApiKey,
        },
      });
      const indices = await result.json();
      setIndices(indices);
    };

    fetchIndices();
  }, [userApiKey]);

  return (
    <div className="flex flex-col mt-6">
      <div className="flex justify-between items-center">
        <div className="flex flex-col">
          <h1 className="text-2xl font-bold">Your indices</h1>
          <p className="text-gray-500 dark:text-gray-400">
            Create an index to start searching
          </p>
        </div>
        <CreateIndexButton />
      </div>

      <div className="mt-6 flex flex-col gap-6">
        {indices.map((index: any) => {
          return (
            <Card href={`/indexes/${index.id}`}>
              <div className="flex flex-col gap-2">
                <h1 className="text-xl font-bold">{index.name}</h1>
                <ClickToCopy text={index.id} />
                <p className="text-gray-500 dark:text-gray-400">
                  Uses{" "}
                  {
                    {
                      milvus: "Milvus",
                      pinecone: "Pinecone",
                    }[index.vector_db.type]
                  }{" "}
                  as vector database and{" "}
                  {
                    {
                      openai: "OpenAI",
                      huggingface: "Hugging Face",
                    }[index.embedding_model.type]
                  }{" "}
                  for generating embeddings.
                </p>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};
