import { useFormContext } from "react-hook-form";
import { Pipeline } from "../types";
import { Label, TextInput } from "flowbite-react";

export const S3TextForm = () => {
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
