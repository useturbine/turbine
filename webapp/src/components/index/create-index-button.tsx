import { Button, Modal } from "flowbite-react";
import { useState } from "react";
import { CreateIndexForm } from "./create-index-form";
import { HiPlus } from "react-icons/hi";

export default function CreateIndexButton() {
  const [modalOpen, setModalOpen] = useState<boolean>(false);

  return (
    <>
      <Button color="blue" onClick={() => setModalOpen(true)}>
        <HiPlus className="mr-2 h-5 w-5" />
        <p>Create Index</p>
      </Button>
      <Modal show={modalOpen} popup onClose={() => setModalOpen(false)}>
        <Modal.Header />
        <Modal.Body>
          <div className="mt-4">
            <CreateIndexForm {...{ setModalOpen }} />
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
}
