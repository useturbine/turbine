import { ApiKey } from "../components/api-key";
import { ListIndices } from "../components/list-indices";

export const Home = () => {
  return (
    <div className="flex flex-col justify-center">
      <ApiKey />
      <ListIndices />
    </div>
  );
};
