import { Tooltip } from "flowbite-react";
import { useCopyToClipboard } from "usehooks-ts";

export const ClickToCopy = ({ text }: { text: string }) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_, copy] = useCopyToClipboard();

  return (
    <Tooltip content="Click to copy">
      <button className="font-mono" onClick={() => copy(text)}>
        {text}
      </button>
    </Tooltip>
  );
};
