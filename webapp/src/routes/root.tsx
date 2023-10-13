import {
  RedirectToSignIn,
  SignedIn,
  SignedOut,
  UserButton,
  useUser,
} from "@clerk/clerk-react";
import { Sidebar } from "flowbite-react";
import { useEffect, useState } from "react";
import { Link, Outlet } from "react-router-dom";
import { turbineAdminApiKey, turbineApiUrl } from "../config";
import { HiDatabase, HiKey } from "react-icons/hi";

export const Root = () => {
  const { user } = useUser();
  const [userApiKey, setUserApiKey] = useState<string | null>(null);

  // Fetch user's API key, keep retrying until it's available
  useEffect(() => {
    const fetchUserApiKey = async () => {
      if (!user) return;

      // eslint-disable-next-line no-constant-condition
      while (true) {
        const result = await fetch(`${turbineApiUrl}/users/${user?.id}`, {
          headers: {
            "X-Turbine-Key": turbineAdminApiKey,
          },
        });
        if (!result.ok) {
          await new Promise((resolve) => setTimeout(resolve, 1000));
          continue;
        }
        const userDetails = await result.json();
        setUserApiKey(userDetails.api_key);
        break;
      }
    };

    fetchUserApiKey();
  }, [user]);

  return (
    <>
      <SignedIn>
        <div className="mx-auto flex h-full pr-10">
          <Sidebar className="h-screen">
            <Sidebar.Logo
              href="#"
              img="/images/turbine-transparent.png"
              imgAlt="Turbine Logo"
            >
              <p>Turbine App</p>
            </Sidebar.Logo>
            <Sidebar.Items>
              <Sidebar.ItemGroup>
                <Sidebar.Item as={Link} href="/" icon={HiDatabase}>
                  <p>Indexes</p>
                </Sidebar.Item>
                <Sidebar.Item href="#" icon={HiKey} active>
                  <p>API Keys</p>
                </Sidebar.Item>
              </Sidebar.ItemGroup>
            </Sidebar.Items>
          </Sidebar>
          <div className="flex flex-col flex-1">
            <div className="flex justify-end mt-4">
              <UserButton afterSignOutUrl="/sign-in" />
            </div>
            <div className="flex flex-1 items-start ml-6">
              <Outlet context={{ userApiKey }} />
            </div>
          </div>
        </div>
      </SignedIn>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
    </>
  );
};
