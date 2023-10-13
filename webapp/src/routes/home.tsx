import { ApiKey } from "../components/api-key";
import { ListIndices } from "../components/list-indices";
import { ListPipelines } from "../components/list-pipelines";

export const Home = () => {
  return (
    <div className="flex flex-col justify-center flex-1">
      {/* <ApiKey /> */}
      <ListIndices />
      {/* <ListPipelines /> */}
    </div>
  );
};
