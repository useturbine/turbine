import { Button, Modal } from "flowbite-react";
import { useState } from "react";
import { CreateIndexForm } from "./create-index-form";

export default function CreateIndexButton() {
  const [openModal, setOpenModal] = useState<string | undefined>();

  return (
    <>
      <Button color="blue" onClick={() => setOpenModal("create-index-form")}>
        Create Index
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
