import { Button, Card } from "flowbite-react";
import { ClickToCopy } from "./click-to-copy";
import axios from "axios";
import { turbineApiUrl } from "../config";
import { useMutation, useQueryClient } from "react-query";
import { useRootContext } from "../utils";
import { HiPlay } from "react-icons/hi";
import { toast } from "react-toastify";

export type PipelineFromAPI = {
  id: string;
  name: string;
  index: string;
  data_source: {
    url: string;
    splitter: {
      size: number;
      overlap: number;
    };
  };
};

// Mutation to run pipeline
const runPipeline = async ({
  pipelineId,
  userApiKey,
}: {
  pipelineId: string;
  userApiKey?: string;
}): Promise<string> => {
  if (!userApiKey) throw new Error("User API key is required");

  const result = await axios.post(
    `${turbineApiUrl}/pipelines/${pipelineId}/run`,
    null,
    {
      headers: {
        "X-Turbine-Key": userApiKey,
      },
    }
  );
  return result.data.id;
};

export const PipelineCard = ({ pipeline }: { pipeline: PipelineFromAPI }) => {
  const { userApiKey } = useRootContext();

  // React Query
  const queryClient = useQueryClient();
  const { mutate, isLoading } = useMutation({
    mutationFn: () => runPipeline({ pipelineId: pipeline.id, userApiKey }),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["tasks", pipeline.index],
      });

      // Show toast
      toast.success("Pipeline started");
    },
  });

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
                <ClickToCopy text={pipeline.data_source.url + "*"} />.
              </li>
              <li>
                Recursively chunks them using chunk size of{" "}
                {pipeline.data_source.splitter.size} characters and chunk
                overlap of {pipeline.data_source.splitter.overlap} characters.
              </li>
            </ul>
          </p>
        </div>
        <div className="flex flex-col gap-2 ml-6">
          <Button
            onClick={() => mutate()}
            isProcessing={isLoading}
            gradientMonochrome="lime"
          >
            <HiPlay className="mr-2 h-5 w-5" />
            <p>Run pipeline</p>
          </Button>
        </div>
      </div>
    </Card>
  );
};
