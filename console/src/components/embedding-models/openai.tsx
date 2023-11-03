import { useFormContext } from "react-hook-form";
import { Index } from "../types";
import { Input } from "@nextui-org/react";

export const OpenAIForm = () => {
  const { register } = useFormContext<Index>();

  return (
    <>
      <Input
        label="OpenAI Model"
        isRequired
        {...register("openaiConfig.model")}
        defaultValue="text-embedding-ada-002"
      />
      <Input
        label="OpenAI API Key"
        isRequired
        {...register("openaiConfig.apiKey")}
      />
    </>
  );
};
