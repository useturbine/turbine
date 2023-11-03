import { useQuery } from "react-query";
import { useRootContext } from "../utils";
import { fetchDataSources } from "../queries";
import { DataSourceCard } from "./data-source-card";
import { Button, Card, CardBody } from "@nextui-org/react";
import { Link } from "react-router-dom";
import { HiPlusCircle } from "react-icons/hi";

// Displays a list of data sources, a card for each
export const DataSourcesList = ({ indexId }: { indexId: string }) => {
  const { userApiKey, externalUserId } = useRootContext();

  // Get pipelines query
  const { data: dataSources } = useQuery(
    ["data-sources", externalUserId, indexId],
    () => fetchDataSources({ userApiKey, indexId }),
    { enabled: !!userApiKey }
  );

  if (!dataSources?.length)
    return (
      <Card className="max-w-md mx-auto">
        <CardBody className="text-center gap-3">
          <p className="text-lg leading-tight">
            You haven't connected any data source yet. Connect one to start
            syncing data.
          </p>
          <div>
            <Button
              color="primary"
              variant="flat"
              as={Link}
              to={`/indexes/${indexId}/connect-data-source`}
              startContent={<HiPlusCircle className="h-5 w-5" />}
            >
              Connect Data Source
            </Button>
          </div>
          <p className="text-md leading-tight">
            You can also upload files directly to the index using the button at
            top right 👀
          </p>
        </CardBody>
      </Card>
    );

  return (
    <div className="flex flex-col gap-2">
      {dataSources?.map((dataSource) => {
        return <DataSourceCard key={dataSource.id} dataSource={dataSource} />;
      })}
    </div>
  );
};
