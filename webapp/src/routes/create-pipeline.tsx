import { Button, Select, Label, TextInput } from "flowbite-react";
import { SubmitHandler, useForm, FormProvider } from "react-hook-form";
import { useRootContext } from "../utils";
import { Pipeline } from "../components/types";
import { PineconeForm } from "../components/vector-dbs";
import { OpenAIForm } from "../components/embedding-models";
import { useMutation, useQueryClient } from "react-query";
import { toast } from "react-toastify";
import { S3TextForm } from "../components/data-sources";
import { createPipeline, runPipeline } from "../components/utils";
import { useNavigate } from "react-router-dom";

const PrivateBetaNotice = () => {
  return (
    <p className="text-md mt-4 text-red-500">
      This feature is currently in private beta. If you would like to try it
      out, please reach out to us on{" "}
      <a
        href="https://discord.gg/5vGGDKV6x"
        target="_blank"
        className="text-blue-500 hover:text-blue-700"
      >
        Discord
      </a>{" "}
      or email us at{" "}
      <a
        href="mailto:sumit@useturbine.com"
        target="_blank"
        className="text-blue-500 hover:text-blue-700"
      >
        sumit@useturbine.com
      </a>
      .
    </p>
  );
};

export const CreatePipeline = () => {
  const { userApiKey, externalUserId } = useRootContext();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  // Run pipeline mutation
  const { mutate: runPipelineMutate } = useMutation({
    mutationFn: (pipelineId: string) =>
      runPipeline({ pipelineId: pipelineId, userApiKey }),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["tasks", externalUserId],
      });
    },
  });

  // Create pipeline mutation
  const {
    mutate: createPipelineMutate,
    isLoading,
    isError,
    error,
  } = useMutation({
    mutationFn: (pipeline: Pipeline) =>
      createPipeline({ pipeline, userApiKey }),
    onSuccess: (pipelineId) => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["pipelines", externalUserId],
      });

      // Run pipeline
      runPipelineMutate(pipelineId);

      // Show success toast
      toast.success("Pipeline created and started");
      navigate(`/pipelines/${pipelineId}`);
    },
  });

  // Form
  const methods = useForm<Pipeline>({
    defaultValues: {
      vectorDatabaseType: "pinecone",
      embeddingModelType: "openai",
      dataSourceType: "s3_text",
      s3TextConfig: {
        chunkSize: 500,
        chunkOverlap: 50,
      },
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
  const onSubmit: SubmitHandler<Pipeline> = (pipeline) =>
    createPipelineMutate(pipeline);

  const VectorDatabaseFormOptions = {
    pinecone: PineconeForm,
    // milvus: MilvusForm,
    milvus: PrivateBetaNotice,
    weaviate: PrivateBetaNotice,
    chroma: PrivateBetaNotice,
  };
  const EmbeddingModelFormOptions = {
    openai: OpenAIForm,
    // huggingface: HuggingFaceForm,
    huggingface: PrivateBetaNotice,
  };
  const DataSourceFormOptions = {
    s3_text: S3TextForm,
    s3_pdf: PrivateBetaNotice,
    postgres: PrivateBetaNotice,
    mongo: PrivateBetaNotice,
    notion: PrivateBetaNotice,
  };
  const VectorDatabaseForm =
    VectorDatabaseFormOptions[watch("vectorDatabaseType")];
  const EmbeddingModelForm =
    EmbeddingModelFormOptions[watch("embeddingModelType")];
  const DataSourceForm = DataSourceFormOptions[watch("dataSourceType")];

  return (
    <div className="flex flex-col gap-10 mt-10 flex-1">
      <div className="flex flex-col gap-2">
        <h1 className="text-2xl font-bold">Create Pipeline</h1>
        <p className="text-gray-500">
          Create a pipeline to start syncing data from any source to any vector
          database. Pipelines are fully configurable, and lets you bring your
          own data source, embedding model, and vector database. After you
          create a pipeline we will automatically trigger a run for you.
        </p>
      </div>
      <FormProvider {...methods}>
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="flex flex-col gap-4 flex-1"
        >
          <div className="flex gap-10 justify-between">
            <div className="flex flex-col flex-1 gap-2">
              <div>
                <div className="mb-1 block">
                  <Label htmlFor="dataSource" value="Select Data Source" />
                </div>
                <Select
                  id="dataSource"
                  required
                  {...register("dataSourceType")}
                >
                  <option value="s3_text">Text files stored on S3</option>
                  <option value="s3_pdf">PDF files stored on S3</option>
                  <option value="postgres">Postgres</option>
                  <option value="mongo">MongoDB</option>
                  <option value="notion">Notion</option>
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
                  <option value="weaviate">Weaviate</option>
                  <option value="chroma">Chroma</option>
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
              helperText="Give a unique name to your pipeline"
            />
          </div>

          <Button type="submit" isProcessing={isLoading}>
            Create Pipeline
          </Button>
          {isError && (
            <div className="text-red-500 dark:text-red-400 mx-auto text-center">
              <p>Something went wrong</p>
              {/* eslint-disable-next-line @typescript-eslint/ban-ts-comment */}
              {/* @ts-expect-error */}
              <p>{error.response?.data.detail}</p>
            </div>
          )}
        </form>
      </FormProvider>
    </div>
  );
};
