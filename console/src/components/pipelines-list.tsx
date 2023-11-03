import { useQuery } from "react-query";
import { useRootContext } from "../utils";
import { fetchPipelines } from "../queries";
import { PipelineCard } from "./pipeline-card";

// Displays a list of pipelines, a card for each pipeline
export const PipelinesList = ({ indexId }: { indexId: string }) => {
  const { userApiKey, externalUserId } = useRootContext();

  // Get pipelines query
  const { data: pipelines } = useQuery(
    ["pipelines", externalUserId, indexId],
    () => fetchPipelines({ userApiKey, indexId }),
    { enabled: !!userApiKey }
  );

  return (
    <div className="flex flex-col gap-2">
      {pipelines?.map((pipeline) => {
        return <PipelineCard key={pipeline.id} pipeline={pipeline} />;
      })}
    </div>
  );
};
