import { useFormContext } from "react-hook-form";
import { Pipeline } from "../types";
import { Input } from "@nextui-org/react";

export const S3Form = () => {
  const { register } = useFormContext<Pipeline>();

  return (
    <>
      <Input
        isRequired
        {...register("s3Config.url")}
        label="S3 URL"
        description="In the format of s3://bucket-name/key-prefix"
      />
      <Input
        isRequired
        type="number"
        min={1}
        placeholder="1024"
        label="Chunk Size"
        {...register("s3Config.chunkSize")}
      />
      <Input
        id="chunkOverlap"
        type="number"
        min={0}
        placeholder="128"
        isRequired
        label="Chunk Overlap"
        {...register("s3Config.chunkOverlap")}
      />
    </>
  );
};
