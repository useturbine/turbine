import { useQuery } from "react-query";
import { fetchIndexes } from "../queries";
import { Link, useParams } from "react-router-dom";
import { useRootContext } from "../utils";
import {
  Button,
  Chip,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
  Tab,
  Tabs,
  useDisclosure,
} from "@nextui-org/react";
import { useState } from "react";
import { TasksTable } from "../components/tasks-table";
import { DeleteIndexModal } from "../components/delete-index-modal";
import { MdOutlineTaskAlt } from "react-icons/md";
import { HiCog, HiDatabase, HiPlusCircle } from "react-icons/hi";
import { DataSourcesList } from "../components/data-sources-list";
import { HiTrash } from "react-icons/hi2";
import { SlOptionsVertical } from "react-icons/sl";
import { FileButton } from "../components/file-button";

export const Index = () => {
  const { userApiKey, externalUserId } = useRootContext();
  const { indexId } = useParams();
  const { isOpen, onOpenChange, onClose, onOpen } = useDisclosure();
  const [selectedTab, setSelectedTab] = useState("data-sources");

  const embeddingModelChipContents = {
    openai: "OpenAI",
    huggingface: "HuggingFace",
  };
  const vectorDatabaseChipContents = {
    pinecone: "Pinecone",
    milvus: "Milvus",
    weaviate: "Weaviate",
  };

  // Get index query
  const { data: indexes } = useQuery(
    ["indexes", externalUserId],
    () => fetchIndexes({ userApiKey }),
    { enabled: !!userApiKey }
  );
  const index = indexes?.find((x) => x.id === indexId);
  if (!index || !indexId) return null;

  return (
    <>
      <DeleteIndexModal {...{ indexId, onClose, onOpenChange, isOpen }} />

      <div className="flex flex-col flex-1 mt-6 ml-6 gap-6">
        <div className="flex justify-between items-start ">
          <div className="flex flex-col gap-1">
            <div className="flex gap-2 items-center">
              <h1 className="text-xl font-bold">Index: {index.name}</h1>
              <Chip className="font-mono" size="sm">
                {embeddingModelChipContents[index.embedding_model.type]}
              </Chip>
              <Chip className="font-mono" size="sm">
                {vectorDatabaseChipContents[index.vector_database.type]}
              </Chip>
            </div>
            <p>
              ID: <span className="font-mono">{index.id} </span>
            </p>
          </div>
          <div className="flex gap-2">
            <Button
              color="primary"
              variant="ghost"
              startContent={<HiPlusCircle className="h-5 w-5" />}
              as={Link}
              to={`/indexes/${index.id}/connect-data-source`}
            >
              Connect Data Source
            </Button>
            <FileButton indexId={index.id} />
            <Dropdown>
              <DropdownTrigger>
                <Button
                  startContent={<SlOptionsVertical className="h5 w-5" />}
                  isIconOnly
                />
              </DropdownTrigger>
              <DropdownMenu
                disabledKeys={["edit"]}
                onAction={(key) => key === "delete" && onOpen()}
              >
                <DropdownItem
                  key="edit"
                  startContent={<HiCog className="h-5 w-5" />}
                >
                  Edit index
                </DropdownItem>
                <DropdownItem
                  key="delete"
                  className="text-danger"
                  color="danger"
                  startContent={<HiTrash className="h-5 w-5" />}
                >
                  Delete index
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </div>
        </div>

        <Tabs
          color="primary"
          size="lg"
          selectedKey={selectedTab}
          // eslint-disable-next-line @typescript-eslint/ban-ts-comment
          // @ts-expect-error
          onSelectionChange={setSelectedTab}
        >
          <Tab
            key="data-sources"
            title={
              <div className="flex items-center space-x-2">
                <HiDatabase className="h-5 w-5" />
                <span>Data Sources</span>
              </div>
            }
          >
            <DataSourcesList indexId={index.id} />
          </Tab>
          <Tab
            key="tasks"
            title={
              <div className="flex items-center space-x-2">
                <MdOutlineTaskAlt className="h-5 w-5" />
                <span>Tasks</span>
              </div>
            }
            className="flex flex-col"
          >
            <TasksTable indexId={index.id} />
          </Tab>
        </Tabs>
      </div>
    </>
  );
};
