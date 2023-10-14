import { useFormContext } from "react-hook-form";
import { Index } from "../types";
import { Label, TextInput } from "flowbite-react";

export const PineconeForm = () => {
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
