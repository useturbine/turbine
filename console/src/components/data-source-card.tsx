import { DataSourceFromAPI, useRootContext } from "../utils";
import { useMutation, useQueryClient } from "react-query";
import { syncDataSource } from "./utils";
import { toast } from "react-toastify";
import { HiPlay, HiCog } from "react-icons/hi";
import { HiTrash } from "react-icons/hi2";
import { DeleteDataSourceModal } from "./delete-data-source-modal";
import {
  Button,
  Card,
  CardBody,
  Chip,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
  useDisclosure,
} from "@nextui-org/react";
import { SlOptionsVertical } from "react-icons/sl";

export const DataSourceCard = ({
  dataSource,
}: {
  dataSource: DataSourceFromAPI;
}) => {
  const { userApiKey, externalUserId } = useRootContext();
  const { isOpen, onOpenChange, onClose, onOpen } = useDisclosure();
  const queryClient = useQueryClient();

  // Sync data source mutation
  const { mutate, isLoading } = useMutation({
    mutationFn: () =>
      syncDataSource({ dataSourceId: dataSource.id, userApiKey }),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["tasks", externalUserId, dataSource.index_id],
      });

      // Show toast
      toast.success("Task to sync data source started");
    },
  });
  const chipContents = {
    s3: "S3",
  };

  return (
    <>
      <DeleteDataSourceModal
        {...{ dataSource, onClose, onOpenChange, isOpen }}
      />

      <Card>
        <CardBody>
          <div className="flex justify-between items-center">
            <div className="flex flex-col gap-1">
              <div className="flex gap-2 items-center">
                <h1 className="text-lg font-bold">{dataSource.name}</h1>
                <Chip className="font-mono" size="sm">
                  {chipContents[dataSource.data_source.type]}
                </Chip>
              </div>
              <span className="text-sm font-mono">{dataSource.id}</span>
            </div>

            <div className="flex gap-2 ml-6">
              <Button
                color="primary"
                variant="ghost"
                startContent={<HiPlay className="h-5 w-5" />}
                onPress={() => mutate()}
                isLoading={isLoading}
              >
                Sync Now
              </Button>
              <Dropdown>
                <DropdownTrigger>
                  <Button
                    startContent={<SlOptionsVertical className="h-4 w-4" />}
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
                    Edit data source
                  </DropdownItem>
                  <DropdownItem
                    key="delete"
                    className="text-danger"
                    color="danger"
                    startContent={<HiTrash className="h-5 w-5" />}
                  >
                    Remove data source
                  </DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </div>
          </div>
        </CardBody>
      </Card>
    </>
  );
};
