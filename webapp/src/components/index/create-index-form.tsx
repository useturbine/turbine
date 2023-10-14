import { Button, Select, Label, TextInput } from "flowbite-react";
import { SubmitHandler, useForm, FormProvider } from "react-hook-form";
import { useRootContext } from "../../utils";
import { turbineApiUrl } from "../../config";
import { Index } from "./types";
import { MilvusForm, PineconeForm } from "./vector-dbs";
import { OpenAIForm, HuggingFaceForm } from "./embedding-models";
import { useMutation, useQueryClient } from "react-query";
import axios from "axios";

// Mutation to create index
const createIndex = async ({
  index,
  userApiKey,
}: {
  index: Index;
  userApiKey?: string;
}) => {
  if (!userApiKey) throw new Error("User API key is required");

  const payload = {
    name: index.name,
    vector_db: {
      type: index.vectorDbType,
      ...(index.vectorDbType === "pinecone"
        ? {
            api_key: index.pineconeConfig.apiKey,
            environment: index.pineconeConfig.environment,
          }
        : {
            url: index.milvusConfig.url,
            token: index.milvusConfig.token,
          }),
    },
    embedding_model: {
      type: index.embeddingModelType,
      ...(index.embeddingModelType === "openai"
        ? {
            model: index.openaiConfig.model,
            api_key: index.openaiConfig.apiKey,
          }
        : {
            model: index.huggingfaceConfig.model,
            token: index.huggingfaceConfig.token,
          }),
    },
    embedding_dimension: index.embeddingDimension,
    similarity_metric: index.similarityMetric,
  };
  const result = await axios.post(`${turbineApiUrl}/indexes`, payload, {
    headers: {
      "X-Turbine-Key": userApiKey,
    },
  });
  return result.data.id;
};

export const CreateIndexForm = () => {
  const { userApiKey, externalUserId } = useRootContext();

  // React Query
  const queryClient = useQueryClient();
  const { mutate, isLoading, isError } = useMutation({
    mutationFn: (index: Index) => createIndex({ index, userApiKey }),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["indexes", externalUserId],
      });
    },
  });

  // Form
  const methods = useForm<Index>({
    defaultValues: {
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

  // Create index using Turbine API
  const onSubmit: SubmitHandler<Index> = (index) => mutate(index);

  return (
    <FormProvider {...methods}>
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col gap-4 justify-between"
      >
        <div className="flex flex-col">
          <h1 className="text-2xl font-bold">Create Index</h1>
          <p className="text-gray-500">Create an index to start searching</p>
        </div>

        <div className="flex gap-10 justify-between">
          <div className="flex flex-col flex-1 gap-2">
            <div>
              <div className="mb-1 block">
                <Label htmlFor="vectorDb" value="Select Vector Database" />
              </div>
              <Select id="vectorDb" required {...register("vectorDbType")}>
                <option hidden disabled selected value="none">
                  Select an option
                </option>
                <option value="pinecone">Pinecone</option>
                <option value="milvus">Milvus</option>
              </Select>
            </div>

            {
              {
                pinecone: <PineconeForm />,
                milvus: <MilvusForm />,
              }[watch("vectorDbType")]
            }
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
                <option hidden disabled selected value="none">
                  Select an option
                </option>
                <option value="openai">OpenAI</option>
                <option value="huggingface">Hugging Face</option>
              </Select>
            </div>

            {
              {
                openai: <OpenAIForm />,
                huggingface: <HuggingFaceForm />,
              }[watch("embeddingModelType")]
            }
          </div>
        </div>

        <div className="flex gap-10 justify-between">
          <div className="flex-1">
            <div className="mb-1 block">
              <Label htmlFor="embeddingDimension" value="Embedding Dimension" />
            </div>
            <TextInput
              id="embeddingDimension"
              required
              type="number"
              min={1}
              max={2048}
              {...register("embeddingDimension", { valueAsNumber: true })}
            />
          </div>
          <div className="flex-1">
            <div className="mb-1 block">
              <Label htmlFor="similarityMetric" value="Similarity Metric" />
            </div>
            <Select
              id="similarityMetric"
              required
              {...register("similarityMetric")}
            >
              <option hidden disabled selected value="none">
                Select an option
              </option>
              <option value="cosine">Cosine</option>
              <option value="euclidean">Euclidean</option>
            </Select>
          </div>
        </div>

        <div>
          <div className="mb-1 block">
            <Label htmlFor="name" value="Name" />
          </div>
          <TextInput
            id="name"
            required
            {...register("name")}
            helperText="Give a name to your index"
          />
        </div>
        <Button type="submit" isProcessing={isLoading}>
          Create Index
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
