import { Button, Select, Label, TextInput } from "flowbite-react";
import {
  SubmitHandler,
  useForm,
  FormProvider,
  useFormContext,
} from "react-hook-form";
import { useRootContext } from "../../utils";
import { turbineApiUrl } from "../../config";
import axios from "axios";
import { useMutation, useQuery, useQueryClient } from "react-query";
import { fetchIndexes } from "../../queries";
import { Dispatch, SetStateAction } from "react";
import { toast } from "react-toastify";

type S3Text = {
  url: string;
  chunkSize: number;
  chunkOverlap: number;
};

type Pipeline = {
  indexId: string;
  name: string;
  dataSourceType: "s3_text";
  s3TextConfig: S3Text;
};

const createPipeline = async ({
  pipeline,
  userApiKey,
}: {
  pipeline: Pipeline;
  userApiKey?: string;
}) => {
  if (!userApiKey) throw new Error("User API key is required");

  const payload = {
    name: pipeline.name,
    index: pipeline.indexId,
    data_source: {
      type: pipeline.dataSourceType,
      ...(pipeline.dataSourceType === "s3_text"
        ? {
            url: pipeline.s3TextConfig.url,
            splitter: {
              type: "recursive",
              size: pipeline.s3TextConfig.chunkSize,
              overlap: pipeline.s3TextConfig.chunkOverlap,
            },
          }
        : {}),
    },
  };
  const result = await axios.post(`${turbineApiUrl}/pipelines`, payload, {
    headers: {
      "X-Turbine-Key": userApiKey,
    },
  });
  return result.data.id;
};

const S3TextForm = () => {
  const { register } = useFormContext<Pipeline>();

  return (
    <>
      <div>
        <div className="mb-1 block">
          <Label htmlFor="url" value="S3 Bucket URL" />
        </div>
        <TextInput
          id="url"
          required
          {...register("s3TextConfig.url")}
          helperText="In the format of s3://bucket-name/key-prefix"
        />
      </div>
      <div>
        <div className="mb-1 block">
          <Label htmlFor="chunkSize" value="Chunk Size" />
        </div>
        <TextInput
          id="chunkSize"
          required
          type="number"
          min={1}
          {...register("s3TextConfig.chunkSize")}
        />
      </div>
      <div>
        <div className="mb-1 block">
          <Label htmlFor="chunkOverlap" value="Chunk Overlap" />
        </div>
        <TextInput
          id="chunkOverlap"
          type="number"
          min={0}
          required
          {...register("s3TextConfig.chunkOverlap")}
        />
      </div>
    </>
  );
};

export const CreatePipelineForm = ({
  indexId,
  setModalOpen,
}: {
  indexId: string;
  setModalOpen: Dispatch<SetStateAction<boolean>>;
}) => {
  const { userApiKey, externalUserId } = useRootContext();
  const methods = useForm<Pipeline>();

  // React Query
  const queryClient = useQueryClient();
  const { mutate, isLoading, isError } = useMutation({
    mutationFn: (pipeline: Pipeline) =>
      createPipeline({ pipeline, userApiKey }),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["pipelines", indexId],
      });

      // Close modal and show success toast
      setModalOpen(false);
      toast.success("Pipeline created");
    },
  });

  // Get index name
  const { data: indexes } = useQuery(
    ["indexes", externalUserId],
    () => fetchIndexes({ userApiKey }),
    { enabled: !!userApiKey }
  );
  const indexName = indexes?.find((index) => index.id === indexId)?.name;

  const onSubmit: SubmitHandler<Pipeline> = (pipeline) =>
    mutate({ ...pipeline, indexId });

  return (
    <FormProvider {...methods}>
      <form
        onSubmit={methods.handleSubmit(onSubmit)}
        className="flex flex-col gap-2"
      >
        <div className="flex flex-col">
          <h1 className="text-2xl font-bold">Create Pipeline</h1>
          <p className="text-gray-500">
            Create a pipeline for index {indexName}
          </p>
        </div>

        <div>
          <div className="mb-1 block">
            <Label htmlFor="name" value="Pipeline Name" />
          </div>
          <TextInput id="name" required {...methods.register("name")} />
        </div>
        <div>
          <div className="mb-1 block">
            <Label htmlFor="dataSourceType" value="Data Source" />
          </div>
          <Select
            id="dataSourceType"
            required
            {...methods.register("dataSourceType")}
          >
            <option value="">Select an option</option>
            <option value="s3_text">Text files stored on S3</option>
          </Select>
        </div>
        {methods.watch("dataSourceType") === "s3_text" && <S3TextForm />}
        <div className="mt-6">
          <Button isProcessing={isLoading} type="submit">
            Create Pipeline
          </Button>
        </div>
        {isError && (
          <p className="text-red-500 dark:text-red-400 mx-auto">
            Something went wrong
          </p>
        )}
      </form>
    </FormProvider>
  );
};
