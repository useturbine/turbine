import { TaskFromAPI, useRootContext } from "../utils";
import { useQuery } from "react-query";
import { fetchTasks } from "../queries";
import {
  Chip,
  Table,
  TableBody,
  TableCell,
  TableColumn,
  TableHeader,
  TableRow,
} from "@nextui-org/react";
import { HiCheck } from "react-icons/hi";
import { FiAlertCircle } from "react-icons/fi";
import { BiLoader } from "react-icons/bi";
import humanizeDuration from "humanize-duration";

const formatDate = (timestamp: string) => {
  const date = new Date(timestamp);
  return date.toLocaleString();
};

const formatTimeElapsed = (start: string, end?: string) => {
  const startTime = new Date(start);
  const endTime = end ? new Date(end) : new Date();
  const diff = startTime.getTime() - endTime.getTime();
  return humanizeDuration(diff, { round: true });
};

const numTasksToShow = 5;

export const TasksTable = ({ indexId }: { indexId: string }) => {
  const { userApiKey, externalUserId } = useRootContext();

  // Get tasks query
  const { data: tasks } = useQuery(
    ["tasks", externalUserId, indexId],
    () => fetchTasks({ userApiKey, indexId }),
    { enabled: !!userApiKey, refetchInterval: 1000 }
  );
  const tasksToShow = tasks
    // ?.filter((task) => task.index_id === indexId)
    ?.sort((a, b) => {
      return (
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
    })
    .slice(0, numTasksToShow);

  const taskStatus = (task: TaskFromAPI) =>
    task.successful ? "successful" : task.finished_at ? "failed" : "running";
  const TaskStatusChips = {
    successful: (
      <Chip
        startContent={<HiCheck className="h-4 w-4" />}
        color="success"
        size="sm"
      >
        Success
      </Chip>
    ),
    failed: (
      <Chip
        startContent={<FiAlertCircle className="h-4 w-4" />}
        color="danger"
        size="sm"
      >
        Failed
      </Chip>
    ),
    running: (
      <Chip startContent={<BiLoader className="h-4 w-4" />} color="primary">
        Running
      </Chip>
    ),
  };
  if (!tasksToShow) return null;

  return (
    <Table>
      <TableHeader>
        <TableColumn>Status</TableColumn>
        <TableColumn>ID</TableColumn>
        <TableColumn>Started at</TableColumn>
        <TableColumn>Time Taken</TableColumn>
      </TableHeader>
      <TableBody emptyContent="No tasks run yet.">
        {tasksToShow.map((task) => {
          return (
            <TableRow key={task.id}>
              <TableCell>{TaskStatusChips[taskStatus(task)]}</TableCell>
              <TableCell>
                <span className="font-mono">{task.id}</span>
              </TableCell>
              <TableCell>{formatDate(task.created_at)}</TableCell>
              <TableCell>
                {formatTimeElapsed(task.created_at, task.finished_at)}
              </TableCell>
            </TableRow>
          );
        })}
      </TableBody>
    </Table>
  );
};
