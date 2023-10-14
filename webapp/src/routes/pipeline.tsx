import { useRootContext } from "../utils";
import { useParams } from "react-router-dom";
import CreatePipelineButton from "../components/pipeline/create-pipeline-button";
import { useQuery } from "react-query";
import { fetchIndexes, fetchPipelines, fetchTasks } from "../queries";
import { PipelineCard } from "../components/pipeline";
import { Tabs } from "flowbite-react";
import { TaskCard } from "../components/task-card";

export const Pipeline = () => {
  const { userApiKey, externalUserId } = useRootContext();
  const { indexId } = useParams();

  const { data: indexes } = useQuery(
    ["indexes", externalUserId],
    () => fetchIndexes({ userApiKey }),
    { enabled: !!userApiKey }
  );
  const index = indexes?.find((index) => index.id === indexId);

  // Fetch pipelines
  const { data: pipelines } = useQuery(
    ["pipelines", indexId],
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-expect-error
    () => fetchPipelines({ userApiKey, indexId }),
    { enabled: !!userApiKey && !!indexId }
  );

  // Fetch tasks
  const { data: tasks } = useQuery(
    ["tasks", indexId],
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-expect-error
    () => fetchTasks({ userApiKey, indexId }),
    { enabled: !!userApiKey && !!indexId, refetchInterval: 1000 }
  );

  return (
    <div className="flex flex-col gap-6 flex-1">
      <div className="flex flex-col gap-2">
        <h1 className="text-xl font-bold">Index: {index?.name}</h1>
        <p className="font-mono">{index?.id}</p>
        <p className="text-gray-500 dark:text-gray-400">
          <ul className="list-disc">
            <li>
              Uses{" "}
              {
                {
                  openai: "OpenAI",
                  huggingface: "Hugging Face",
                }[index?.embedding_model.type as "openai" | "huggingface"]
              }{" "}
              to generate embeddings.
            </li>
            <li>
              Uses{" "}
              {
                {
                  milvus: "Milvus",
                  pinecone: "Pinecone",
                }[index?.vector_db.type as "milvus" | "pinecone"]
              }{" "}
              as the vector database.
            </li>
          </ul>
        </p>
      </div>
      <Tabs.Group aria-label="Default tabs" style="default">
        <Tabs.Item active title="Pipelines">
          <div className="flex flex-col gap-6">
            <div className="flex justify-between items-center">
              <div className="flex flex-col">
                <h1 className="text-2xl font-bold">Your pipelines</h1>
                <p className="text-gray-500 dark:text-gray-400">
                  Create a pipeline to start chunking documents
                </p>
              </div>
              <CreatePipelineButton indexId={indexId!} />
            </div>
            {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
            {pipelines?.map((pipeline: any) => {
              return <PipelineCard pipeline={pipeline} />;
            })}
          </div>
        </Tabs.Item>
        <Tabs.Item title="Pipeline Runs">
          {tasks?.map((task) => {
            return <TaskCard task={task} />;
          })}
        </Tabs.Item>
      </Tabs.Group>
    </div>
  );
};
