import { Button, Card, Dropdown, Modal } from "flowbite-react";
import { ClickToCopy } from "./click-to-copy";
import { useMutation, useQueryClient } from "react-query";
import { PipelineFromAPI, useRootContext } from "../utils";
import {
  HiDotsVertical,
  HiOutlineExclamationCircle,
  HiPlay,
  HiTrash,
} from "react-icons/hi";
import { toast } from "react-toastify";
import { deletePipeline, runPipeline } from "./utils";
import { useState } from "react";

const DeletePipelineModal = ({
  pipeline,
  deleteModalOpen,
  setDeleteModalOpen,
}: {
  pipeline: PipelineFromAPI;
  deleteModalOpen: boolean;
  setDeleteModalOpen: (value: boolean) => void;
}) => {
  const { userApiKey, externalUserId } = useRootContext();

  // React Query
  const queryClient = useQueryClient();
  const { mutate, isLoading } = useMutation({
    mutationFn: () => deletePipeline({ pipelineId: pipeline.id, userApiKey }),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["pipelines", externalUserId],
      });

      // Close modal and show toast
      setDeleteModalOpen(false);
      toast.success("Pipeline deleted");
    },
  });

  return (
    <Modal
      show={deleteModalOpen}
      size="md"
      popup
      onClose={() => setDeleteModalOpen(false)}
    >
      <Modal.Header />
      <Modal.Body>
        <div className="text-center">
          <HiOutlineExclamationCircle className="mx-auto mb-4 h-14 w-14 text-gray-400 dark:text-gray-200" />
          <h3 className="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
            Are you sure you want to delete this pipeline?
          </h3>
          <div className="flex justify-center gap-4">
            <Button
              color="failure"
              onClick={() => mutate()}
              isProcessing={isLoading}
            >
              Yes, I'm sure
            </Button>
            <Button color="gray" onClick={() => setDeleteModalOpen(false)}>
              No, cancel
            </Button>
          </div>
        </div>
      </Modal.Body>
    </Modal>
  );
};

export const PipelineCard = ({ pipeline }: { pipeline: PipelineFromAPI }) => {
  const { userApiKey, externalUserId } = useRootContext();
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);

  // React Query
  const queryClient = useQueryClient();
  const { mutate, isLoading } = useMutation({
    mutationFn: () => runPipeline({ pipelineId: pipeline.id, userApiKey }),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["tasks", externalUserId],
      });

      // Show toast
      toast.success("Pipeline started");
    },
  });

  return (
    <>
      <DeletePipelineModal
        {...{ pipeline, deleteModalOpen, setDeleteModalOpen }}
      />
      <Card>
        <div className="flex justify-between items-start">
          <div className="flex flex-col gap-2">
            <h1 className="text-xl font-bold">{pipeline.name}</h1>
            <ClickToCopy text={pipeline.id} />
            <p className="text-gray-500 dark:text-gray-400">
              <ul className="list-disc">
                <li>
                  Takes documents from{" "}
                  <ClickToCopy text={pipeline.data_source.url + "*"} />.
                </li>
                <li>
                  Recursively chunks them using chunk size of{" "}
                  {pipeline.data_source.splitter.size} characters and chunk
                  overlap of {pipeline.data_source.splitter.overlap} characters.
                </li>

                <li>
                  Uses{" "}
                  {
                    {
                      openai: "OpenAI",
                      huggingface: "Hugging Face",
                    }[pipeline.embedding_model.type as "openai" | "huggingface"]
                  }{" "}
                  to generate embeddings.
                </li>
                <li>
                  Stores embeddings to{" "}
                  {
                    {
                      milvus: "Milvus",
                      pinecone: "Pinecone",
                    }[pipeline.vector_database.type as "milvus" | "pinecone"]
                  }{" "}
                  vector database.
                </li>
              </ul>
            </p>
          </div>

          <div className="flex gap-2 ml-6">
            <Button
              onClick={() => mutate()}
              isProcessing={isLoading}
              gradientMonochrome="lime"
            >
              <HiPlay className="mr-2 h-5 w-5" />
              <p>Run pipeline</p>
            </Button>
            <Dropdown label={<HiDotsVertical />} inline dismissOnClick={false}>
              <Dropdown.Item
                icon={HiTrash}
                onClick={() => setDeleteModalOpen(true)}
              >
                Delete pipeline
              </Dropdown.Item>
            </Dropdown>
          </div>
        </div>
      </Card>
    </>
  );
};
