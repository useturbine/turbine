import { Badge, Card } from "flowbite-react";
import { ClickToCopy } from "./click-to-copy";

const formatDate = (timestamp: string) => {
  const date = new Date(timestamp);
  return date.toLocaleString();
};

export const TaskCard = ({
  task,
}: {
  task: {
    id: string;
    successful: boolean;
    created_at: string;
    finished_at?: string;
  };
}) => {
  return (
    <Card>
      <div className="flex flex-col ">
        <div className="flex gap-4 items-center">
          <ClickToCopy text={task.id} />
          {task.successful ? (
            <Badge color="green">Successful</Badge>
          ) : task.finished_at ? (
            <Badge color="red">Failed</Badge>
          ) : (
            <Badge color="yellow">Running</Badge>
          )}
        </div>

        <p className="text-gray-500 dark:text-gray-400">
          <p>Created at {formatDate(task.created_at)}</p>
          {task.finished_at && (
            <p>Finished at {formatDate(task.finished_at)}</p>
          )}
        </p>
      </div>
    </Card>
  );
};
