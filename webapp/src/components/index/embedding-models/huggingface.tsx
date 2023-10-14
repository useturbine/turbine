import { useFormContext } from "react-hook-form";
import { Index } from "../types";
import { Label, TextInput } from "flowbite-react";

export const HuggingFaceForm = () => {
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
