import { useRootContext } from "../utils";
import { Button } from "flowbite-react";
import { fetchPipelines } from "../queries";
import { useQuery } from "react-query";
import { HiPlus } from "react-icons/hi";
import { PipelineCard } from "../components/pipeline-card";
import { Link } from "react-router-dom";

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
          Pipelines are the core offering of this app. Create a pipeline to
          start syncing data from any source to any vector database. Pipelines
          are fully configurable, and lets you bring your own data source,
          embedding model, and vector database.
        </p>
        <p className="text-gray-500 dark:text-gray-400">
          Following are the pipelines you have created. Click on a pipeline to
          view its details and run it. If you're new here, start by{" "}
          <Link
            to="/create-pipeline"
            className="text-blue-500 hover:text-blue-700 underline"
          >
            creating a pipeline
          </Link>
          .
        </p>

        <div className="flex flex-1 justify-end">
          <Button
            color="blue"
            href="/create-pipeline"
            className="whitespace-nowrap"
          >
            <HiPlus className="mr-2 h-5 w-5" />
            <span>Create Pipeline</span>
          </Button>
        </div>
      </div>

      <div className="mt-6 flex flex-col gap-6">
        {pipelines?.map((pipeline) => {
          return <PipelineCard key={pipeline.id} pipeline={pipeline} />;
        })}
      </div>
    </div>
  );
};
