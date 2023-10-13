import { useEffect, useState } from "react";
import { useRootContext } from "../utils";
import { turbineApiUrl } from "../config";
import { Accordion, Button } from "flowbite-react";
import CreatePipelineButton from "./create-pipeline-button";

export const ListPipelines = () => {
  const [pipelines, setPipelines] = useState([]);
  const [loading, setLoading] = useState(false);
  const { userApiKey } = useRootContext();

  // Fetch pipelines created by the user
  useEffect(() => {
    const fetchPipelines = async () => {
      if (!userApiKey) return;

      const result = await fetch(`${turbineApiUrl}/pipelines`, {
        headers: {
          "X-Turbine-Key": userApiKey,
        },
      });
      const pipelines = await result.json();
      setPipelines(pipelines);
    };

    fetchPipelines();
  }, [userApiKey]);

  // Run pipeline using Turbine API
  const runPipeline = async (pipelineId: string) => {
    if (!userApiKey) return;
    setLoading(true);

    try {
      const result = await fetch(
        `${turbineApiUrl}/pipelines/${pipelineId}/run`,
        {
          method: "POST",
          headers: {
            "X-Turbine-Key": userApiKey,
          },
        }
      );
      const response = await result.json();

      if (!result.ok) {
        console.error(response);
      }
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col mt-6">
      <div className="flex justify-between items-center">
        <div className="flex flex-col">
          <h1 className="text-2xl font-bold">Your pipelines</h1>
          <p className="text-gray-500 dark:text-gray-400">
            Create a pipeline to start processing
          </p>
        </div>
        <CreatePipelineButton />
      </div>

      <Accordion collapseAll className="mt-6">
        {pipelines.map((pipeline: any) => {
          return (
            <Accordion.Panel>
              <Accordion.Title>{pipeline.name}</Accordion.Title>
              <Accordion.Content>
                <div className="flex gap-4">
                  <pre className="text-gray-500 dark:text-gray-400 flex-1">
                    {JSON.stringify(pipeline, null, 2)}
                  </pre>
                  <div className="flex flex-col gap-2 justify-end">
                    <Button
                      color="dark"
                      isProcessing={loading}
                      onClick={() => runPipeline(pipeline.id)}
                    >
                      Run Pipeline
                    </Button>
                    <Button disabled color="warning">
                      Delete Pipeline
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
