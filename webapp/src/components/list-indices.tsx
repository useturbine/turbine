import { useEffect, useState } from "react";
import { useRootContext } from "../utils";
import { turbineApiUrl } from "../config";
import { Accordion, Button } from "flowbite-react";
import CreateIndexButton from "./create-index-button";

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

      <Accordion collapseAll className="mt-6">
        {indices.map((index: any) => {
          return (
            <Accordion.Panel>
              <Accordion.Title>{index.name}</Accordion.Title>
              <Accordion.Content>
                <div className="flex gap-4">
                  <pre className="text-gray-500 dark:text-gray-400 flex-1">
                    {JSON.stringify(index, null, 2)}
                  </pre>
                  <div className="flex flex-col gap-2 justify-end">
                    <Button disabled color="warning">
                      Delete Index
                    </Button>
                  </div>
                </div>
              </Accordion.Content>
            </Accordion.Panel>
          );
        })}
      </Accordion>
    </div>
  );
};
