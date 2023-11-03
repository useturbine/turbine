import { Button } from "@nextui-org/react";
import { useRef } from "react";
import { BsFillArrowUpCircleFill } from "react-icons/bs";
import { useMutation, useQueryClient } from "react-query";
import { toast } from "react-toastify";
import { useRootContext } from "../utils";
import { uploadFiles } from "./utils";

export const FileButton = ({ indexId }: { indexId: string }) => {
  const { userApiKey, externalUserId } = useRootContext();
  const inputRef = useRef<HTMLInputElement>(null);

  const queryClient = useQueryClient();
  const { mutate, isLoading } = useMutation({
    mutationFn: (files: File[]) => uploadFiles({ indexId, userApiKey, files }),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["tasks", externalUserId, indexId],
      });

      // Close modal and show toast
      toast.success("Task to index files started");
    },
  });

  const onFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    console.log(files);
    if (!files) return;
    mutate([...files]);
  };

  return (
    <>
      <Button
        color="primary"
        variant="flat"
        startContent={<BsFillArrowUpCircleFill className="h-4 w-4" />}
        onClick={() => inputRef.current?.click()}
        isLoading={isLoading}
      >
        Upload Files
      </Button>
      <input
        type="file"
        className="hidden"
        onChange={onFileSelect}
        ref={inputRef}
        multiple={true}
      />
    </>
  );
};
