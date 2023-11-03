import {
  RedirectToSignIn,
  SignedIn,
  SignedOut,
  UserButton,
  useUser,
} from "@clerk/clerk-react";
import { Button, Image } from "@nextui-org/react";
import { Link, Outlet, useNavigate } from "react-router-dom";
import { HiCog, HiOutlinePlusCircle } from "react-icons/hi";
import { ReactQueryDevtools } from "react-query/devtools";
import { ToastContainer } from "react-toastify";
import { useQuery } from "react-query";
import { fetchUserApiKey } from "../queries";
import "react-toastify/dist/ReactToastify.css";
import { FaDiscord, FaListUl } from "react-icons/fa";
import { TbApi } from "react-icons/tb";

const SidebarLink = ({
  path,
  children,
  icon,
}: {
  path: string;
  icon?: React.ReactNode;
  children: React.ReactNode;
}) => {
  const navigate = useNavigate();

  return (
    <Button
      size="lg"
      variant={location.pathname == path ? "flat" : "light"}
      radius="sm"
      startContent={icon}
      onPress={() => navigate(path)}
      className="justify-start"
    >
      <div className="text-md text-left">{children}</div>
    </Button>
  );
};

export const Root = () => {
  const { user } = useUser();
  const externalUserId = user?.id;

  const { data: userApiKey } = useQuery(
    ["userApiKey", externalUserId],
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-expect-error
    () => fetchUserApiKey({ externalUserId }),
    { enabled: !!externalUserId }
  );

  return (
    <>
      <ReactQueryDevtools initialIsOpen={false} />
      <SignedIn>
        <ToastContainer
          position="bottom-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="light"
        />
        <div className="flex flex-col">
          <nav className="flex justify-between items-center gap-2 py-3 px-4 border-b">
            <div className="flex items-center gap-2">
              <Image src="/images/turbine-transparent.png" width="30px" />
              <h1 className="text-xl font-semibold italic font-mono tracking-tighter">
                Turbine Console
              </h1>
            </div>

            <div className="flex items-center">
              <Button
                variant="light"
                as={Link}
                to="https://api.useturbine.com/docs"
                startContent={<TbApi className="h-6 w-6" />}
                target="_blank"
              >
                Visit API Docs
              </Button>
              <Button
                color="primary"
                variant="light"
                as={Link}
                to="https://api.useturbine.com/docs"
                startContent={<FaDiscord className="h-6 w-6" />}
                target="_blank"
              >
                Join Discord
              </Button>
              <div className="px-2">
                <UserButton afterSignOutUrl="/sign-in" />
              </div>
            </div>
          </nav>

          <div className="flex h-screen">
            <div className="flex flex-col gap-2 p-4 border-r">
              <SidebarLink path="/" icon={<FaListUl className="h-5 w-5" />}>
                Indexes
              </SidebarLink>
              <SidebarLink
                path="/create-index"
                icon={<HiOutlinePlusCircle className="h-5 w-5" />}
              >
                Create Index
              </SidebarLink>
              <SidebarLink
                path="/settings"
                icon={<HiCog className="h-5 w-5" />}
              >
                Settings
              </SidebarLink>
            </div>

            <main className="flex flex-col flex-1 pr-10">
              <div className="flex flex-1 items-start ml-6">
                <Outlet context={{ userApiKey: userApiKey, externalUserId }} />
              </div>
            </main>
          </div>
        </div>
      </SignedIn>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
    </>
  );
};
