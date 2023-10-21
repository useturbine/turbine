import { Badge, Table } from "flowbite-react";
import { ClickToCopy } from "./click-to-copy";
import { TaskFromAPI } from "../utils";
import { HiCheck } from "react-icons/hi";
import { BiLoader } from "react-icons/bi";
import { FiAlertCircle } from "react-icons/fi";

const formatDate = (timestamp: string) => {
  const date = new Date(timestamp);
  return date.toLocaleString();
};

export const TaskRow = ({ task }: { task: TaskFromAPI }) => {
  const taskStatus = task.successful
    ? "successful"
    : task.finished_at
    ? "failed"
    : "running";
  const StatusOptions = {
    successful: (
      <Badge icon={HiCheck} color="success" size="xs">
        Success
      </Badge>
    ),
    failed: (
      <Badge icon={FiAlertCircle} color="failure">
        Failed
      </Badge>
    ),
    running: (
      <Badge icon={BiLoader} color="warning">
        Running
      </Badge>
    ),
  };
  const Status = StatusOptions[taskStatus];

  return (
    <Table.Row className="bg-white dark:border-gray-700 dark:bg-gray-800">
      <Table.Cell>{Status}</Table.Cell>
      <Table.Cell>
        <ClickToCopy text={task.id} />
      </Table.Cell>
      <Table.Cell>{formatDate(task.created_at)}</Table.Cell>
      <Table.Cell>
        {task.finished_at && formatDate(task.finished_at)}
      </Table.Cell>
    </Table.Row>
  );
};
