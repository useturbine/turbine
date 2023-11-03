import { Select, SelectItem, Input, Button } from "@nextui-org/react";
import { SubmitHandler, useForm, FormProvider } from "react-hook-form";
import { useRootContext } from "../utils";
import { Index } from "../components/types";
import { PineconeForm } from "../components/vector-databases";
import { OpenAIForm } from "../components/embedding-models";
import { useMutation, useQueryClient } from "react-query";
import { toast } from "react-toastify";
import { createIndex } from "../components/utils";
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

export const CreateIndex = () => {
  const { userApiKey, externalUserId } = useRootContext();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  // Create index mutation
  const { mutate, isLoading, isError } = useMutation({
    mutationFn: (index: Index) => createIndex({ index, userApiKey }),
    onSuccess: (indexId) => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["indexes", externalUserId],
      });

      // Show success toast
      toast.success("Index created");
      navigate(`/indexes/${indexId}`);
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

  // Handle form submit
  const onSubmit: SubmitHandler<Index> = (index) => mutate(index);

  const VectorDatabaseFormOptions = {
    pinecone: PineconeForm,
    milvus: PrivateBetaNotice,
    weaviate: PrivateBetaNotice,
    chroma: PrivateBetaNotice,
  };
  const EmbeddingModelFormOptions = {
    openai: OpenAIForm,
    huggingface: PrivateBetaNotice,
  };

  const NullElement = () => <></>;
  const VectorDatabaseForm =
    VectorDatabaseFormOptions[watch("vectorDatabaseType")] || NullElement;
  const EmbeddingModelForm =
    EmbeddingModelFormOptions[watch("embeddingModelType")] || NullElement;

  return (
    <div className="flex flex-col gap-4 mt-6 w-full mx-auto max-w-3xl">
      <h1 className="text-2xl font-bold ml-1">Create Index</h1>

      <FormProvider {...methods}>
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="flex flex-col flex-1 gap-4"
        >
          <div className="flex gap-10 justify-between">
            <div className="flex flex-col flex-1 gap-2">
              <Select
                id="embeddingModel"
                isRequired
                {...register("embeddingModelType")}
                label="Select Embedding Model"
                color="primary"
              >
                <SelectItem key="openai" value="openai">
                  OpenAI
                </SelectItem>
                <SelectItem key="huggingface" value="huggingface">
                  Hugging Face
                </SelectItem>
              </Select>
              <EmbeddingModelForm />
            </div>

            <div className="flex flex-col flex-1 gap-2">
              <Select
                id="vectorDatabase"
                isRequired
                {...register("vectorDatabaseType")}
                label="Select Vector Database"
                color="primary"
              >
                <SelectItem key="pinecone" value="pinecone">
                  Pinecone
                </SelectItem>
                <SelectItem key="milvus" value="milvus">
                  Milvus
                </SelectItem>
                <SelectItem key="weaviate" value="weaviate">
                  Weaviate
                </SelectItem>
                <SelectItem key="chroma" value="chroma">
                  Chroma
                </SelectItem>
              </Select>
              <VectorDatabaseForm />
            </div>
          </div>

          <div className="flex flex-col items-start gap-4">
            <Input
              isRequired
              label="Index Name"
              {...register("name")}
              placeholder="My Index"
            />

            <Button
              type="submit"
              isLoading={isLoading}
              color="primary"
              variant="shadow"
              size="lg"
            >
              Create Index
            </Button>
          </div>

          {isError && (
            <div className="text-red-500 dark:text-red-400 mx-auto text-center">
              <p>Something went wrong</p>
            </div>
          )}
        </form>
      </FormProvider>
    </div>
  );
};
