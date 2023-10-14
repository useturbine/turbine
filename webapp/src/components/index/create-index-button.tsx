import { Button, Modal } from "flowbite-react";
import { useState } from "react";
import { CreateIndexForm } from "./create-index-form";
import { HiPlus } from "react-icons/hi";

export default function CreateIndexButton() {
  const [openModal, setOpenModal] = useState<string | undefined>();

  return (
    <>
      <Button color="blue" onClick={() => setOpenModal("create-index-form")}>
        <HiPlus className="mr-2 h-5 w-5" />
        <p>Create Index</p>
      </Button>
      <Modal
        show={openModal === "create-index-form"}
        popup
        onClose={() => setOpenModal(undefined)}
      >
        <Modal.Header />
        <Modal.Body>
          <div className="mt-4">
            <CreateIndexForm />
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
}
