import { useMutation, useQueryClient } from "react-query";
import { toast } from "react-toastify";
import { deleteIndex } from "./utils";
import { useNavigate } from "react-router-dom";
import { HiOutlineExclamationCircle } from "react-icons/hi";
import { useRootContext } from "../utils";
import {
  Button,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
} from "@nextui-org/react";

export const DeleteIndexModal = ({
  indexId,
  isOpen,
  onOpenChange,
  onClose,
}: {
  indexId: string;
  isOpen: boolean;
  onOpenChange: (value: boolean) => void;
  onClose: () => void;
}) => {
  const { userApiKey, externalUserId } = useRootContext();
  const navigate = useNavigate();

  // React Query
  const queryClient = useQueryClient();
  const { mutate, isLoading } = useMutation({
    mutationFn: () => deleteIndex({ indexId, userApiKey }),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({
        queryKey: ["indexes", externalUserId],
      });

      // Close modal and show toast
      onClose();
      toast.success("Index deleted");
      navigate("/");
    },
  });

  return (
    <Modal backdrop="opaque" isOpen={isOpen} onOpenChange={onOpenChange}>
      <ModalContent>
        {(onClose) => (
          <>
            <ModalHeader>
              <div className="flex items-center justify-start gap-2">
                <HiOutlineExclamationCircle className="h-6 w-6" />
                <span>Delete Index</span>
              </div>
            </ModalHeader>
            <ModalBody>
              <div className="text-center">
                <div className="flex mb-4">
                  <h3 className="text-lg">
                    Are you sure you want to delete this index?
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
