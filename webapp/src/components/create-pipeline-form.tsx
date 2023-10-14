import { Button, Select, Label, TextInput } from "flowbite-react";
import { SubmitHandler, useForm, FormProvider } from "react-hook-form";
import { useRootContext } from "../utils";
import { Pipeline } from "./types";
import { MilvusForm, PineconeForm } from "./vector-dbs";
import { OpenAIForm, HuggingFaceForm } from "./embedding-models";
import { useMutation, useQueryClient } from "react-query";
import { toast } from "react-toastify";
import { S3TextForm } from "./data-sources";
import { createPipeline } from "./utils";

export const CreatePipelineForm = () => {
  const { userApiKey, externalUserId } = useRootContext();

  // React Query
  const queryClient = useQueryClient();
  const { mutate, isLoading, isError } = useMutation({
    mutationFn: (pipeline: Pipeline) =>
      createPipeline({ pipeline, userApiKey }),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["pipelines", externalUserId],
      });

      // Show success toast
      toast.success("Pipeline created");
    },
  });

  // Form
  const methods = useForm<Pipeline>({
    defaultValues: {
      vectorDatabaseType: "pinecone",
      embeddingModelType: "openai",
      dataSourceType: "s3_text",
      openaiConfig: {
        model: "text-embedding-ada-002",
      },
    },
  });
  const {
    register,
    handleSubmit,
    watch,
    // formState: { errors },
  } = methods;

  // Handle form submit
  const onSubmit: SubmitHandler<Pipeline> = (pipeline) => mutate(pipeline);

  const VectorDatabaseFormOptions = {
    pinecone: PineconeForm,
    milvus: MilvusForm,
  };
  const EmbeddingModelFormOptions = {
    openai: OpenAIForm,
    huggingface: HuggingFaceForm,
  };
  const DataSourceFormOptions = {
    s3_text: S3TextForm,
  };
  const VectorDatabaseForm =
    VectorDatabaseFormOptions[watch("vectorDatabaseType")];
  const EmbeddingModelForm =
    EmbeddingModelFormOptions[watch("embeddingModelType")];
  const DataSourceForm = DataSourceFormOptions[watch("dataSourceType")];

  return (
    <FormProvider {...methods}>
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col gap-4 justify-between flex-1"
      >
        <div className="flex flex-col">
          <h1 className="text-2xl font-bold">Create Pipeline</h1>
          <p className="text-gray-500">
            Create a pipeline to start syncing your data
          </p>
        </div>

        <div className="flex gap-10 justify-between">
          <div className="flex flex-col flex-1 gap-2">
            <div>
              <div className="mb-1 block">
                <Label htmlFor="dataSource" value="Select Data Source" />
              </div>
              <Select id="dataSource" required {...register("dataSourceType")}>
                <option value="s3_text">Text files stored on S3</option>
              </Select>
            </div>

            <DataSourceForm />
          </div>

          <div className="flex flex-col flex-1 gap-2">
            <div>
              <div className="mb-1 block">
                <Label
                  htmlFor="embeddingModel"
                  value="Select Embedding Model"
                />
              </div>
              <Select
                id="embeddingModel"
                required
                {...register("embeddingModelType")}
              >
                <option value="openai">OpenAI</option>
                <option value="huggingface">Hugging Face</option>
              </Select>
            </div>

            <EmbeddingModelForm />
          </div>

          <div className="flex flex-col flex-1 gap-2">
            <div>
              <div className="mb-1 block">
                <Label
                  htmlFor="vectorDatabase"
                  value="Select Vector Database"
                />
              </div>
              <Select
                id="vectorDatabase"
                required
                {...register("vectorDatabaseType")}
              >
                <option value="pinecone">Pinecone</option>
                <option value="milvus">Milvus</option>
              </Select>
            </div>

            <VectorDatabaseForm />
          </div>
        </div>

        <div>
          <div className="mb-1 block">
            <Label htmlFor="pipelineName" value="Name" />
          </div>
          <TextInput
            id="pipelineName"
            required
            {...register("name")}
            helperText="Give a name to your pipeline"
          />
        </div>

        <Button type="submit" isProcessing={isLoading}>
          Create Pipeline
        </Button>
        {isError && (
          <p className="text-red-500 dark:text-red-400 mx-auto">
            Something went wrong
          </p>
        )}
      </form>
    </FormProvider>
  );
};
