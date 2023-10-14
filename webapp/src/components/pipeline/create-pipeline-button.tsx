import { Button, Modal } from "flowbite-react";
import { useState } from "react";
import { CreatePipelineForm } from "./create-pipeline-form";
import { HiPlus } from "react-icons/hi";

export default function CreatePipelineButton({ indexId }: { indexId: string }) {
  const [modalOpen, setModalOpen] = useState<boolean>(false);

  return (
    <>
      <Button color="blue" onClick={() => setModalOpen(true)}>
        <HiPlus className="mr-2 h-5 w-5" />
        <p>Create Pipeline</p>
      </Button>
      <Modal show={modalOpen} popup onClose={() => setModalOpen(false)}>
        <Modal.Header />
        <Modal.Body>
          <div className="mt-4">
            <CreatePipelineForm {...{ indexId, setModalOpen }} />
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
}
