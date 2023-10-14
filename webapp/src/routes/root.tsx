import {
  RedirectToSignIn,
  SignedIn,
  SignedOut,
  UserButton,
  useUser,
} from "@clerk/clerk-react";
import { Sidebar } from "flowbite-react";
import { Outlet, useLocation } from "react-router-dom";
import { HiDatabase, HiKey, HiPlus } from "react-icons/hi";
import { ReactQueryDevtools } from "react-query/devtools";
import { ToastContainer } from "react-toastify";
import { useQuery } from "react-query";
import { fetchUserApiKey } from "../queries";
import "react-toastify/dist/ReactToastify.css";

export const Root = () => {
  const { user } = useUser();
  const externalUserId = user?.id;

  const location = useLocation();
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
        <div className="flex">
          <Sidebar className="h-screen sticky top-0">
            <Sidebar.Logo
              href="#"
              img="/images/turbine-transparent.png"
              imgAlt="Turbine Logo"
            >
              <p>Turbine App</p>
            </Sidebar.Logo>
            <Sidebar.Items>
              <Sidebar.ItemGroup>
                <Sidebar.Item
                  href="/"
                  icon={HiDatabase}
                  active={location.pathname === "/"}
                >
                  <p>Pipelines</p>
                </Sidebar.Item>
                <Sidebar.Item
                  href="/create-pipeline"
                  icon={HiPlus}
                  active={location.pathname === "/create-pipeline"}
                >
                  <p>Create Pipeline</p>
                </Sidebar.Item>
                <Sidebar.Item
                  href="/keys"
                  icon={HiKey}
                  active={location.pathname === "/keys"}
                >
                  <p>API Keys</p>
                </Sidebar.Item>
              </Sidebar.ItemGroup>
            </Sidebar.Items>
          </Sidebar>
          <main className="flex flex-col flex-1 pr-10">
            <div className="flex justify-end mt-4">
              <UserButton afterSignOutUrl="/sign-in" />
            </div>
            <div className="flex flex-1 items-start ml-6">
              <Outlet context={{ userApiKey: userApiKey, externalUserId }} />
            </div>
          </main>
        </div>
      </SignedIn>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
    </>
  );
};
