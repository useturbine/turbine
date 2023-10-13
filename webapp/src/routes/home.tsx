import { ApiKey } from "../components/api-key";
import { CreateIndexForm } from "../components/create-index-form";

export const Home = () => {
  return (
    <div className="flex flex-col justify-center">
      <ApiKey />
      <CreateIndexForm />
    </div>
  );
};
