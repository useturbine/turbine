import { useEffect, useState } from "react";
import { useRootContext } from "../utils";
import { turbineApiUrl } from "../config";
import { Card } from "flowbite-react";
import CreateIndexButton from "../components/create-index-button";

export const Home = () => {
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
    <div className="flex flex-col mt-6 flex-1">
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
        {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
        {indices.map((index: any) => {
          return (
            <Card href={`/indexes/${index.id}`}>
              <div className="flex flex-col gap-2">
                <h1 className="text-xl font-bold">{index.name}</h1>
                <p className="font-mono">{index.id}</p>
                <p className="text-gray-500 dark:text-gray-400">
                  <ul className="list-disc">
                    <li>
                      Uses{" "}
                      {
                        {
                          openai: "OpenAI",
                          huggingface: "Hugging Face",
                        }[
                          index.embedding_model.type as "openai" | "huggingface"
                        ]
                      }{" "}
                      to generate embeddings.
                    </li>
                    <li>
                      Uses{" "}
                      {
                        {
                          milvus: "Milvus",
                          pinecone: "Pinecone",
                        }[index.vector_db.type as "milvus" | "pinecone"]
                      }{" "}
                      as the vector database.
                    </li>
                  </ul>
                </p>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};
