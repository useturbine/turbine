import { Tooltip } from "flowbite-react";
import { useRootContext } from "../utils";
import { useCopyToClipboard } from "usehooks-ts";

export const ApiKey = () => {
  const { userApiKey } = useRootContext();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_, copy] = useCopyToClipboard();

  return (
    <div className="flex items-center mt-4">
      {userApiKey ? (
        <div className="flex gap-1">
          <p>Your API key is</p>
          <Tooltip content="Click to copy">
            <button className="font-mono" onClick={() => copy(userApiKey)}>
              {userApiKey}
            </button>
          </Tooltip>
        </div>
      ) : (
        <p>Your API key is loading...</p>
      )}
    </div>
  );
};
