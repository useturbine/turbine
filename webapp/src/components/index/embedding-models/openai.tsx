import { useFormContext } from "react-hook-form";
import { Index } from "../types";
import { Label, TextInput } from "flowbite-react";

export const OpenAIForm = () => {
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
