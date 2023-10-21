import { useRootContext } from "../utils";
import { Button, Card } from "flowbite-react";
import { fetchPipelines } from "../queries";
import { useQuery } from "react-query";
import { HiPlusCircle } from "react-icons/hi";
import { PipelineCard } from "../components/pipeline-card";

export const Home = () => {
  const { userApiKey, externalUserId } = useRootContext();
  const { data: pipelines } = useQuery(
    ["pipelines", externalUserId],
    () => fetchPipelines({ userApiKey }),
    { enabled: !!userApiKey }
  );

  return (
    <div className="flex flex-col mt-6 flex-1">
      <div className="flex flex-col gap-2">
        <h1 className="text-2xl font-bold">Your pipelines</h1>
        <p className="text-gray-500 dark:text-gray-400">
          Create a pipeline to start syncing data from any source to any vector
          database. Pipelines are fully configurable, and lets you bring your
          own data source, embedding model, and vector database.
        </p>
        <div className="flex flex-1 justify-end">
          <Button
            color="blue"
            href="/create-pipeline"
            className="whitespace-nowrap"
          >
            <HiPlusCircle className="mr-2 h-5 w-5" />
            <span>Create Pipeline</span>
          </Button>
        </div>
      </div>

      {pipelines?.length === 0 && (
        <Card className="max-w-sm mx-auto text-center">
          <p className="text-xl tracking-tight text-gray-900 dark:text-white">
            You haven't created any pipelines yet. Create one to get started.
          </p>
          <Button
            color="blue"
            href="/create-pipeline"
            className="whitespace-nowrap"
          >
            <HiPlusCircle className="mr-2 h-5 w-5" />
            <span>Create Pipeline</span>
          </Button>
        </Card>
      )}

      <div className="mt-6 flex flex-col gap-6">
        {pipelines?.map((pipeline) => {
          return <PipelineCard key={pipeline.id} pipeline={pipeline} />;
        })}
      </div>
    </div>
  );
};
