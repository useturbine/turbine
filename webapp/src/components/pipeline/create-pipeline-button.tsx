import { Button, Modal } from "flowbite-react";
import { useState } from "react";
import { CreatePipelineForm } from "./create-pipeline-form";
import { HiPlus } from "react-icons/hi";

export default function CreatePipelineButton({ indexId }: { indexId: string }) {
  const [openModal, setOpenModal] = useState<string | undefined>();

  return (
    <>
      <Button color="blue" onClick={() => setOpenModal("create-pipeline-form")}>
        <HiPlus className="mr-2 h-5 w-5" />
        <p>Create Pipeline</p>
      </Button>
      <Modal
        show={openModal === "create-pipeline-form"}
        popup
        onClose={() => setOpenModal(undefined)}
      >
        <Modal.Header />
        <Modal.Body>
          <div className="mt-4">
            <CreatePipelineForm {...{ indexId }} />
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
}
