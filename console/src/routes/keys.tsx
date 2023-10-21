import { useRootContext } from "../utils";
import { ClickToCopy } from "../components/click-to-copy";

export const Keys = () => {
  const { userApiKey } = useRootContext();

  return (
    <div className="flex items-center mt-4">
      <p>
        Your API key is <ClickToCopy text={userApiKey!} />.
      </p>
    </div>
  );
};
