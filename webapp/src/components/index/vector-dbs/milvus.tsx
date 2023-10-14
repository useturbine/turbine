import { useFormContext } from "react-hook-form";
import { Index } from "../types";
import { Label, TextInput } from "flowbite-react";

export const MilvusForm = () => {
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
