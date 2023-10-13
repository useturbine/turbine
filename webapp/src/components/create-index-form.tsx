import { Button, Select, Label, TextInput } from "flowbite-react";
import {
  SubmitHandler,
  useForm,
  FormProvider,
  useFormContext,
} from "react-hook-form";
import { useRootContext } from "../utils";
import { useState } from "react";
import { turbineApiUrl } from "../config";

type HuggingFace = {
  model: string;
  token: string;
};

type OpenAI = {
  model: string;
  apiKey: string;
};

type Milvus = {
  url: string;
  token: string;
};

type Pinecone = {
  apiKey: string;
  environment: string;
};

type Index = {
  name: string;
  vectorDbType: "milvus" | "pinecone";
  embeddingModelType: "huggingface" | "openai";
  milvusConfig: Milvus;
  pineconeConfig: Pinecone;
  openaiConfig: OpenAI;
  huggingfaceConfig: HuggingFace;
  embeddingDimension: number;
  similarityMetric: string;
};

const MilvusForm = () => {
  const { register } = useFormContext<Index>();

  return (
    <>
      <div>
        <div className="mb-1 block">
          <Label htmlFor="url" value="Milvus URL" />
        </div>
        <TextInput id="url" required {...register("milvusConfig.url")} />
      </div>
      <div>
        <div className="mb-1 block">
          <Label htmlFor="token" value="Milvus Token" />
        </div>
        <TextInput id="token" {...register("milvusConfig.token")} />
      </div>
    </>
  );
};

const PineconeForm = () => {
  const { register } = useFormContext<Index>();

  return (
    <>
      <div>
        <div className="mb-1 block">
          <Label htmlFor="apiKey" value="Pinecone API Key" />
        </div>
        <TextInput
          id="apiKey"
          required
          {...register("pineconeConfig.apiKey")}
        />
      </div>

      <div>
        <div className="mb-1 block">
          <Label htmlFor="environment" value="Pinecone Environment" />
        </div>
        <TextInput
          id="environment"
          required
          {...register("pineconeConfig.environment")}
        />
      </div>
    </>
  );
};

const HuggingFaceForm = () => {
  const { register } = useFormContext<Index>();

  return (
    <>
      <div>
        <div className="mb-1 block">
          <Label htmlFor="model" value="Hugging Face Model" />
        </div>
        <TextInput
          id="model"
          required
          {...register("huggingfaceConfig.model")}
        />
      </div>

      <div>
        <div className="mb-1 block">
          <Label htmlFor="token" value="Hugging Face Token" />
        </div>
        <TextInput
          id="token"
          required
          {...register("huggingfaceConfig.token")}
        />
      </div>
    </>
  );
};

const OpenAIForm = () => {
  const { register } = useFormContext<Index>();

  return (
    <>
      <div>
        <div className="mb-1 block">
          <Label htmlFor="model" value="OpenAI Model" />
        </div>
        <TextInput id="model" required {...register("openaiConfig.model")} />
      </div>

      <div>
        <div className="mb-1 block">
          <Label htmlFor="apiKey" value="OpenAI API Key" />
        </div>
        <TextInput id="apiKey" required {...register("openaiConfig.apiKey")} />
      </div>
    </>
  );
};

export const CreateIndexForm = () => {
  const { userApiKey } = useRootContext();
  const [isLoading, setIsLoading] = useState(false);

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
  const onSubmit: SubmitHandler<Index> = (data) => {
    try {
      setIsLoading(true);
      fetch(`${turbineApiUrl}/indices`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Turbine-Key": userApiKey!,
        },
        body: JSON.stringify({
          name: data.name,
          vector_db: {
            type: data.vectorDbType,
            ...(data.vectorDbType === "pinecone"
              ? {
                  api_key: data.pineconeConfig.apiKey,
                  environment: data.pineconeConfig.environment,
                }
              : {
                  url: data.milvusConfig.url,
                  token: data.milvusConfig.token,
                }),
          },
          embedding_model: {
            type: data.embeddingModelType,
            ...(data.embeddingModelType === "openai"
              ? {
                  model: data.openaiConfig.model,
                  api_key: data.openaiConfig.apiKey,
                }
              : {
                  model: data.huggingfaceConfig.model,
                  token: data.huggingfaceConfig.token,
                }),
          },
          embedding_dimension: data.embeddingDimension,
          similarity_metric: data.similarityMetric,
        }),
      });
    } catch (error) {
      console.error(error);
    }

    setIsLoading(false);
  };

  return (
    <FormProvider {...methods}>
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col gap-4 mt-10 justify-between"
      >
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

        <Button className="mt-4" type="submit" isProcessing={isLoading}>
          Create Index
        </Button>
      </form>
    </FormProvider>
  );
};
