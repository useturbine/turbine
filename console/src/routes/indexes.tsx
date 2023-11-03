import { useRootContext } from "../utils";
import { Button, Card, CardBody } from "@nextui-org/react";
import { fetchIndexes } from "../queries";
import { useQuery } from "react-query";
import { HiPlusCircle } from "react-icons/hi";
import { IndexCard } from "../components/index-card";
import { Link } from "react-router-dom";

export const Indexes = () => {
  const { userApiKey, externalUserId } = useRootContext();
  const { data: indexes } = useQuery(
    ["indexes", externalUserId],
    () => fetchIndexes({ userApiKey }),
    { enabled: !!userApiKey }
  );

  return (
    <div className="flex flex-col mt-6 flex-1">
      {indexes?.length != undefined && indexes?.length > 0 && (
        <>
          <div className="flex justify-between">
            <h1 className="text-2xl font-bold">Indexes</h1>
            <Button
              color="primary"
              variant="ghost"
              startContent={<HiPlusCircle className="h-5 w-5" />}
              as={Link}
              to="/create-index"
            >
              Create Index
            </Button>
          </div>

          <div className="mt-6 flex flex-col gap-6">
            {indexes?.map((index) => {
              return <IndexCard key={index.id} index={index} />;
            })}
          </div>
        </>
      )}

      {indexes?.length === 0 && (
        <Card className="max-w-sm mx-auto mt-10">
          <CardBody className="text-center gap-3">
            <p className="text-xl">
              You haven't created any index yet. Create one to get started.
            </p>
            <div>
              <Button
                color="primary"
                variant="shadow"
                as={Link}
                to="/create-index"
                startContent={<HiPlusCircle className="h-5 w-5" />}
              >
                Create Index
              </Button>
            </div>
          </CardBody>
        </Card>
      )}
    </div>
  );
};
