import { Button, Select, Label, TextInput } from "flowbite-react";
import {
  SubmitHandler,
  useForm,
  FormProvider,
  useFormContext,
} from "react-hook-form";
import { useRootContext } from "../utils";
import { useEffect, useState } from "react";
import { turbineApiUrl } from "../config";

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

export const CreatePipelineForm = () => {
  const [error, setError] = useState<string>();
  const [loading, setLoading] = useState<boolean>(false);
  const { userApiKey } = useRootContext();
  const methods = useForm<Pipeline>();
  const [indices, setIndices] = useState([]);

  // Fetch indices created by the user
  useEffect(() => {
    const fetchIndices = async () => {
      if (!userApiKey) return;

      const result = await fetch(`${turbineApiUrl}/indices`, {
        headers: {
          "X-Turbine-Key": userApiKey,
        },
      });
      const indices = await result.json();
      setIndices(indices);
    };

    fetchIndices();
  }, [userApiKey]);

  const onSubmit: SubmitHandler<Pipeline> = async (data) => {
    if (!userApiKey) return;
    setLoading(true);
    setError(undefined);

    try {
      const result = await fetch(`${turbineApiUrl}/pipelines`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Turbine-Key": userApiKey,
        },
        body: JSON.stringify({
          name: data.name,
          index: data.indexId,
          data_source: {
            type: data.dataSourceType,
            ...(data.dataSourceType === "s3_text"
              ? {
                  url: data.s3TextConfig.url,
                  splitter: {
                    type: "recursive",
                    size: data.s3TextConfig.chunkSize,
                    overlap: data.s3TextConfig.chunkOverlap,
                  },
                }
              : {}),
          },
        }),
      });

      const response = await result.json();

      if (!result.ok) {
        setError("Something went wrong");
        console.log(response);
        setLoading(false);
        return;
      }
    } catch (error) {
      console.log(error);
      setError(error.message);
    }

    setLoading(false);
  };

  return (
    <FormProvider {...methods}>
      <form
        onSubmit={methods.handleSubmit(onSubmit)}
        className="flex flex-col gap-2"
      >
        <div>
          <div className="mb-1 block">
            <Label htmlFor="name" value="Pipeline Name" />
          </div>
          <TextInput id="name" required {...methods.register("name")} />
        </div>
        <div>
          <div className="mb-1 block">
            <Label htmlFor="indexId" value="Index" />
          </div>
          <Select id="indexId" required {...methods.register("indexId")}>
            {indices.map((index: any) => {
              return <option value={index.id}>{index.name}</option>;
            })}
          </Select>
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
          <Button isProcessing={loading} type="submit">
            Create Pipeline
          </Button>
        </div>
        {error && (
          <p className="text-red-500 dark:text-red-400 mx-auto">{error}</p>
        )}
      </form>
    </FormProvider>
  );
};
