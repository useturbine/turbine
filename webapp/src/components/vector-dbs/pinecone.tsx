import { useFormContext } from "react-hook-form";
import { Pipeline } from "../types";
import { Label, TextInput } from "flowbite-react";

export const PineconeForm = () => {
  const { register } = useFormContext<Pipeline>();

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

      <div>
        <div className="mb-1 block">
          <Label htmlFor="indexName" value="Index Name" />
        </div>
        <TextInput
          id="indexName"
          required
          {...register("pineconeConfig.indexName")}
        />
      </div>
    </>
  );
};
