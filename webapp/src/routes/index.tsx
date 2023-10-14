import { useRootContext } from "../utils";
import { useParams } from "react-router-dom";
import CreatePipelineButton from "../components/pipeline/create-pipeline-button";
import { useQuery } from "react-query";
import { fetchPipelines } from "../queries";
import { PipelineCard } from "../components/pipeline";

export const Index = () => {
  const { userApiKey } = useRootContext();
  const { indexId } = useParams();

  const { data: pipelines } = useQuery(
    ["pipelines", indexId],
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-expect-error
    () => fetchPipelines({ userApiKey, indexId }),
    { enabled: !!userApiKey && !!indexId }
  );

  return (
    <div className="mt-6 flex flex-col gap-6 flex-1">
      <div className="flex justify-between items-center">
        <div className="flex flex-col">
          <h1 className="text-2xl font-bold">Your pipelines</h1>
          <p className="text-gray-500 dark:text-gray-400">
            Create a pipeline to start chunking documents
          </p>
        </div>
        <CreatePipelineButton {...{ indexId }} />
      </div>
      {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
      {pipelines?.map((pipeline: any) => {
        return <PipelineCard pipeline={pipeline} />;
      })}
    </div>
  );
};
