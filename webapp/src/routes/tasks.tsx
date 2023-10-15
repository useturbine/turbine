import { useRootContext } from "../utils";
import { useQuery } from "react-query";
import { fetchTasks } from "../queries";
import { TaskRow } from "../components/task-row";
import { Table } from "flowbite-react";

export const Tasks = () => {
  const { userApiKey, externalUserId } = useRootContext();

  // Fetch tasks
  const { data: tasks } = useQuery(
    ["tasks", externalUserId],
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-expect-error
    () => fetchTasks({ userApiKey }),
    { enabled: !!userApiKey, refetchInterval: 1000 }
  );
  const sortedTasks = tasks?.sort((a, b) => {
    return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
  });

  return (
    <div className="flex flex-col gap-6 flex-1">
      <div className="flex flex-col gap-2">
        <h1 className="text-xl font-bold">Tasks</h1>
        <p className="text-gray-500 dark:text-gray-400">
          Tasks are used to sync your data.
        </p>
      </div>
      <Table hoverable>
        <Table.Head>
          <Table.HeadCell>Status</Table.HeadCell>
          <Table.HeadCell>ID</Table.HeadCell>
          <Table.HeadCell>Description</Table.HeadCell>
          <Table.HeadCell>Started at</Table.HeadCell>
          <Table.HeadCell>Finished at</Table.HeadCell>
        </Table.Head>
        <Table.Body className="divide-y">
          {sortedTasks?.map((task) => {
            return <TaskRow task={task} />;
          })}
        </Table.Body>
      </Table>
    </div>
  );
};
