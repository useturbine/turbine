import { Tooltip } from "@nextui-org/react";
import { useCopyToClipboard } from "usehooks-ts";

export const ClickToCopy = ({ text }: { text: string }) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_, copy] = useCopyToClipboard();

  return (
    <span className="inline-block">
      <Tooltip content="Click to copy">
        <button
          className="font-mono inline-block outline-none"
          onClick={() => copy(text)}
        >
          {text}
        </button>
      </Tooltip>
    </span>
  );
};
