import { useRootContext } from "../utils";
import { useQuery } from "react-query";
import { fetchTasks } from "../queries";
import { TaskCard } from "../components/task-card";

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

  return (
    <div className="flex flex-col gap-6 flex-1">
      <div className="flex flex-col gap-2">
        <h1 className="text-xl font-bold">Tasks</h1>
        <p className="text-gray-500 dark:text-gray-400">
          Tasks are used to sync your data.
        </p>
      </div>
      {tasks?.map((task) => {
        return <TaskCard task={task} />;
      })}
    </div>
  );
};
