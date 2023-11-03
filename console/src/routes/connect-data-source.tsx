import { Select, SelectItem, Input, Button, Link } from "@nextui-org/react";
import { SubmitHandler, useForm, FormProvider } from "react-hook-form";
import { useRootContext } from "../utils";
import { DataSource } from "../components/types";
import { useMutation, useQuery, useQueryClient } from "react-query";
import { toast } from "react-toastify";
import { createDataSource } from "../components/utils";
import { useNavigate, useParams, Link as LinkRouter } from "react-router-dom";
import { S3Form } from "../components/data-sources";
import { fetchIndexes } from "../queries";

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

export const ConnectDataSource = () => {
  const { userApiKey, externalUserId } = useRootContext();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { indexId } = useParams();

  // Get index query
  const { data: indexes } = useQuery(
    ["indexes", externalUserId],
    () => fetchIndexes({ userApiKey }),
    { enabled: !!userApiKey }
  );
  const index = indexes?.find((x) => x.id === indexId);

  // Create data source mutation
  const { mutate, isLoading, isError } = useMutation({
    mutationFn: (dataSource: DataSource) =>
      createDataSource({ dataSource, userApiKey, indexId }),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["pipelines", externalUserId, indexId],
      });

      // Show success toast
      toast.success("Data source connected");
      navigate(`/indexes/${indexId}`);
    },
  });

  // Form
  const methods = useForm<DataSource>({
    defaultValues: {
      s3Config: {
        // chunkSize: 1024,
        // chunkOverlap: 64,
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
  const onSubmit: SubmitHandler<DataSource> = (dataSource) =>
    mutate(dataSource);

  const FormOptions = {
    s3: S3Form,
    mongo: PrivateBetaNotice,
    postgres: PrivateBetaNotice,
    notion: PrivateBetaNotice,
  };
  const NullElement = () => <></>;
  const Form = FormOptions[watch("dataSourceType")] || NullElement;

  return (
    <div className="flex flex-col gap-4 mt-6 w-full mx-auto max-w-3xl">
      <h1 className="text-xl font-bold ml-1">
        Connect Data Source to Index{" "}
        <Link className="text-xl" as={LinkRouter} to={"/indexes/" + indexId}>
          {index?.name}
        </Link>
      </h1>

      <FormProvider {...methods}>
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="flex flex-col flex-1 gap-4"
        >
          <div className="flex flex-col flex-1 gap-2">
            <Select
              isRequired
              {...register("dataSourceType")}
              label="Select Data Source"
              color="primary"
            >
              <SelectItem key="s3" value="s3">
                S3
              </SelectItem>
              <SelectItem key="postgres" value="postgres">
                PostgreSQL
              </SelectItem>
              <SelectItem key="mongo" value="mongo">
                MongoDB
              </SelectItem>
              <SelectItem key="notion" value="notion">
                Notion
              </SelectItem>
            </Select>
            <Form />
          </div>

          <Input
            isRequired
            label="Data Source Name"
            {...register("name")}
            placeholder="My data source"
          />
          <div className="flex justify-start">
            <Button
              type="submit"
              isLoading={isLoading}
              color="primary"
              variant="shadow"
              size="lg"
            >
              Connect Data Source
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
