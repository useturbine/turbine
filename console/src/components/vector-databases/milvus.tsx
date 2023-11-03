import { useFormContext } from "react-hook-form";
import { DataSource } from "../types";

export const MilvusForm = () => {
  const { register } = useFormContext<DataSource>();

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

      <div>
        <div className="mb-1 block">
          <Label htmlFor="collectionName" value="Collection Name" />
        </div>
        <TextInput
          id="collectionName"
          required
          {...register("milvusConfig.collectionName")}
        />
      </div>
    </>
  );
};
