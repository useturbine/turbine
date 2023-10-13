import { useEffect, useState } from "react";
import { useRootContext } from "../utils";
import { turbineApiUrl } from "../config";
import { useParams } from "react-router-dom";
import { Button, Card } from "flowbite-react";
import { ClickToCopy } from "../components/click-to-copy";
import CreatePipelineButton from "../components/create-pipeline-button";

export const Index = () => {
  const [pipelines, setPipelines] = useState([]);
  const [loading, setLoading] = useState(false);
  const { userApiKey } = useRootContext();
  const { indexId } = useParams();

  // Fetch pipelines created by the user
  useEffect(() => {
    const fetchPipelines = async () => {
      if (!userApiKey) return;

      const result = await fetch(
        `${turbineApiUrl}/pipelines?index=${indexId}`,
        {
          headers: {
            "X-Turbine-Key": userApiKey,
          },
        }
      );
      const pipelines = await result.json();
      setPipelines(pipelines);
    };

    fetchPipelines();
  }, [userApiKey, indexId]);

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
    <div className="mt-6 flex flex-col gap-6 flex-1">
      <div className="flex justify-between items-center">
        <div className="flex flex-col">
          <h1 className="text-2xl font-bold">Your pipelines</h1>
          <p className="text-gray-500 dark:text-gray-400">
            Create a pipeline to start chunking documents
          </p>
        </div>
        <CreatePipelineButton />
      </div>
      {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
      {pipelines.map((pipeline: any) => {
        return (
          <Card>
            <div className="flex justify-between">
              <div className="flex flex-col gap-2">
                <h1 className="text-xl font-bold">{pipeline.name}</h1>
                <ClickToCopy text={pipeline.id} />
                <p className="text-gray-500 dark:text-gray-400">
                  <ul className="list-disc">
                    <li>
                      Takes documents from{" "}
                      <ClickToCopy text={pipeline.data_source.url} />.
                    </li>
                    <li>
                      Recursively chunks them using chunk size of{" "}
                      {pipeline.data_source.splitter.size} characters and chunk
                      overlap of {pipeline.data_source.splitter.overlap}{" "}
                      characters.
                    </li>
                    <li>Stores them into this index.</li>
                  </ul>
                </p>
              </div>
              <div className="flex flex-col gap-2 ml-6">
                <Button
                  onClick={() => runPipeline(pipeline.id)}
                  isProcessing={loading}
                  gradientMonochrome="lime"
                >
                  Run pipeline
                </Button>
              </div>
            </div>
          </Card>
        );
      })}
    </div>
  );
};
