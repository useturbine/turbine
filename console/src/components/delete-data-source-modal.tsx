import { useMutation, useQueryClient } from "react-query";
import { toast } from "react-toastify";
import { deleteDataSource } from "./utils";
import { useNavigate } from "react-router-dom";
import { HiOutlineExclamationCircle } from "react-icons/hi";
import { DataSourceFromAPI, useRootContext } from "../utils";
import {
  Button,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
} from "@nextui-org/react";

export const DeleteDataSourceModal = ({
  dataSource,
  isOpen,
  onOpenChange,
  onClose,
}: {
  dataSource: DataSourceFromAPI;
  isOpen: boolean;
  onOpenChange: (value: boolean) => void;
  onClose: () => void;
}) => {
  const { userApiKey, externalUserId } = useRootContext();
  const navigate = useNavigate();

  // React Query
  const queryClient = useQueryClient();
  const { mutate, isLoading } = useMutation({
    mutationFn: () =>
      deleteDataSource({ dataSourceId: dataSource.id, userApiKey }),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["data-sources", externalUserId, dataSource.index_id],
      });

      // Close modal and show toast
      onClose();
      toast.success("Data source removed");
      navigate("/indexes/" + dataSource.index_id);
    },
  });

  return (
    <Modal
      backdrop="opaque"
      size="lg"
      isOpen={isOpen}
      onOpenChange={onOpenChange}
    >
      <ModalContent>
        {(onClose) => (
          <>
            <ModalHeader>
              <div className="flex items-center justify-start gap-2">
                <HiOutlineExclamationCircle className="h-6 w-6" />
                <span>Remove Data Source</span>
              </div>
            </ModalHeader>
            <ModalBody>
              <div className="text-center">
                <div className="flex mb-4">
                  <h3 className="text-lg">
                    Are you sure you want to remove this data source?
                  </h3>
                </div>
              </div>
            </ModalBody>
            <ModalFooter>
              <Button
                color="danger"
                variant="light"
                onClick={() => mutate()}
                isLoading={isLoading}
              >
                Yes, I'm sure
              </Button>
              <Button onClick={onClose} color="primary">
                No, cancel
              </Button>
            </ModalFooter>
          </>
        )}
      </ModalContent>
    </Modal>
  );
};
