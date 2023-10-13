import { Button } from "flowbite-react";
import { useRootContext } from "../utils";
import { useCopyToClipboard } from "usehooks-ts";

export const ApiKey = () => {
  const { userApiKey } = useRootContext();
  const [value, copy] = useCopyToClipboard();

  return (
    <div className="flex justify-center items-center">
      {userApiKey ? (
        <>
          <p>
            Your API key is <span className="font-mono">{userApiKey}</span>
          </p>
          <Button onClick={() => copy(userApiKey)} className="ml-3" size="sm">
            Copy
          </Button>
        </>
      ) : (
        <p>Your API key is loading...</p>
      )}
    </div>
  );
};
