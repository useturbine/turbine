import { useFormContext } from "react-hook-form";
import { Pipeline } from "../types";
import { Input } from "@nextui-org/react";

export const PineconeForm = () => {
  const { register } = useFormContext<Pipeline>();

  return (
    <>
      <Input
        label="Pinecone API Key"
        isRequired
        {...register("pineconeConfig.apiKey")}
      />
      <Input
        isRequired
        label="Pinecone Environment"
        {...register("pineconeConfig.environment")}
      />
      <Input
        isRequired
        label="Pinecone Index Name"
        {...register("pineconeConfig.indexName")}
      />
    </>
  );
};
