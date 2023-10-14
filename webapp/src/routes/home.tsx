import { useRootContext } from "../utils";
import { Button } from "flowbite-react";
import { fetchPipelines } from "../queries";
import { useQuery } from "react-query";
import { HiPlus } from "react-icons/hi";
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
      <div className="flex justify-between items-center">
        <div className="flex flex-col">
          <h1 className="text-2xl font-bold">Your pipelines</h1>
          <p className="text-gray-500 dark:text-gray-400">
            Pipelines are used to sync your data to the index.
          </p>
        </div>
        <Button color="blue" href="/create-pipeline">
          <HiPlus className="mr-2 h-5 w-5" />
          <p>Create Pipeline</p>
        </Button>
      </div>

      <div className="mt-6 flex flex-col gap-6">
        {pipelines?.map((pipeline) => {
          return <PipelineCard key={pipeline.id} pipeline={pipeline} />;
        })}
      </div>
    </div>
  );
};
