import { useMutation, useQuery, useQueryClient } from "react-query";
import { fetchPipelines, fetchTasks } from "../queries";
import { useNavigate, useParams } from "react-router-dom";
import { PipelineFromAPI, useRootContext } from "../utils";
import { ClickToCopy } from "../components/click-to-copy";
import { Breadcrumb, Button, Dropdown, Modal, Table } from "flowbite-react";
import {
  HiDotsVertical,
  HiOutlineExclamationCircle,
  HiPlay,
  HiTrash,
} from "react-icons/hi";
import { FaListUl } from "react-icons/fa";
import { toast } from "react-toastify";
import { deletePipeline, runPipeline } from "../components/utils";
import { useState } from "react";
import { TaskRow } from "../components/task-row";

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
  const navigate = useNavigate();

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
      navigate("/pipelines");
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

const getDescriptions = (pipeline: PipelineFromAPI) => {
  const dataSourceDescriptions = {
    s3_text: pipeline.data_source.type == "s3_text" && (
      <p>
        Takes text files from S3 bucket{" "}
        <span className="font-mono">{pipeline.data_source.url}</span>*.
      </p>
    ),
  };

  const splitterDescriptions = {
    s3_text: pipeline.data_source.type == "s3_text" && (
      <p>
        Recursively chunks them using chunk size of{" "}
        {pipeline.data_source.splitter.size} characters and chunk overlap of{" "}
        {pipeline.data_source.splitter.overlap} characters.
      </p>
    ),
  };

  const embeddingModelDescriptions = {
    openai: pipeline.embedding_model.type == "openai" && (
      <p>
        Uses OpenAI's{" "}
        <span className="font-mono">{pipeline.embedding_model.model}</span>{" "}
        model to generate embeddings.
      </p>
    ),
    huggingface: pipeline.embedding_model.type == "huggingface" && (
      <p>
        Uses Hugging Face's{" "}
        <span className="font-mono">{pipeline.embedding_model.model}</span> to
        generate embeddings.
      </p>
    ),
  };

  const vectorDatabaseDescriptions = {
    milvus: pipeline.vector_database.type == "milvus" && (
      <p>
        Stores embeddings to Milvus at{" "}
        <span className="font-mono">{pipeline.vector_database.url}</span> in
        collection{" "}
        <span className="font-mono">
          {pipeline.vector_database.collection_name}
        </span>
        .
      </p>
    ),
    pinecone: pipeline.vector_database.type == "pinecone" && (
      <p>
        Stores embeddings to Pinecone index{" "}
        <span className="font-mono">{pipeline.vector_database.index_name}</span>
        .
      </p>
    ),
  };

  return {
    dataSourceDescription: dataSourceDescriptions[pipeline.data_source.type],
    embeddingModelDescription:
      embeddingModelDescriptions[pipeline.embedding_model.type],
    vectorDatabaseDescription:
      vectorDatabaseDescriptions[pipeline.vector_database.type],
    splitterDescription: splitterDescriptions[pipeline.data_source.type],
  };
};

export const Pipeline = () => {
  const { userApiKey, externalUserId } = useRootContext();
  const { pipelineId } = useParams();
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const queryClient = useQueryClient();

  // Run pipeline mutation
  const { mutate, isLoading } = useMutation({
    mutationFn: () => runPipeline({ pipelineId: pipelineId!, userApiKey }),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["tasks", externalUserId],
      });

      // Show toast
      toast.success("Pipeline started");
    },
  });

  // Get pipeline query
  const { data: pipelines } = useQuery(
    ["pipelines", externalUserId],
    () => fetchPipelines({ userApiKey }),
    { enabled: !!userApiKey }
  );
  const pipeline = pipelines?.find((p) => p.id === pipelineId);

  // Get tasks query
  const { data: tasks } = useQuery(
    ["tasks", externalUserId],
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-expect-error
    () => fetchTasks({ userApiKey }),
    { enabled: !!userApiKey, refetchInterval: 1000 }
  );
  const numTasksToShow = 5;
  const tasksToShow = tasks
    ?.filter((task) => task.pipeline === pipelineId)
    .sort((a, b) => {
      return (
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
    })
    .slice(0, numTasksToShow);

  if (!pipeline) return null;

  const {
    dataSourceDescription,
    embeddingModelDescription,
    vectorDatabaseDescription,
    splitterDescription,
  } = getDescriptions(pipeline);

  return (
    <>
      <DeletePipelineModal
        {...{ pipeline, deleteModalOpen, setDeleteModalOpen }}
      />

      <div className="flex flex-col flex-1 mt-10 ml-6 gap-6">
        <Breadcrumb aria-label="Default breadcrumb example">
          <Breadcrumb.Item href="/" icon={FaListUl}>
            <p>Pipelines</p>
          </Breadcrumb.Item>
          <Breadcrumb.Item>{pipeline.name}</Breadcrumb.Item>
        </Breadcrumb>

        <div className="flex justify-between items-start ">
          <div className="flex flex-col gap-2">
            <h1 className="text-xl font-bold">Pipeline: {pipeline.name}</h1>
            <p>
              ID: <ClickToCopy text={pipeline.id} />
            </p>
            <p className="text-gray-500 dark:text-gray-400">
              <ul className="list-disc pl-4">
                <li>{dataSourceDescription}</li>
                <li>{splitterDescription} </li>
                <li>{embeddingModelDescription}</li>
                <li>{vectorDatabaseDescription}</li>
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

        <div>
          <h2 className="text-xl font-bold">Recent pipeline runs</h2>
          <p className="text-gray-500 dark:text-gray-400">
            Below you can see the most recent pipeline run tasks and their
            details.
          </p>
        </div>

        <Table hoverable>
          <Table.Head>
            <Table.HeadCell>Status</Table.HeadCell>
            <Table.HeadCell>ID</Table.HeadCell>
            <Table.HeadCell>Started at</Table.HeadCell>
            <Table.HeadCell>Finished at</Table.HeadCell>
          </Table.Head>
          <Table.Body className="divide-y">
            {tasksToShow?.map((task) => {
              return <TaskRow task={task} />;
            })}
          </Table.Body>
        </Table>
      </div>
    </>
  );
};
