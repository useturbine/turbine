import {
  RedirectToSignIn,
  SignedIn,
  SignedOut,
  UserButton,
  useUser,
} from "@clerk/clerk-react";
import { Navbar } from "flowbite-react";
import { useEffect, useState } from "react";
import { Link, Outlet } from "react-router-dom";
import { turbineAdminApiKey, turbineApiUrl } from "../config";

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
      }
    };

    fetchUserApiKey();
  }, [user]);

  return (
    <>
      <SignedIn>
        <div className="mx-auto max-w-6xl">
          <Navbar fluid rounded>
            <Navbar.Brand as={Link} href="https://app.useturbine.com">
              <img
                src="/images/turbine.png"
                className="mr-3 h-6 sm:h-9"
                alt="Turbine Logo"
              />
              <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
                Turbine App
              </span>
            </Navbar.Brand>
            <UserButton afterSignOutUrl="/sign-in" />
          </Navbar>
          <Outlet context={{ userApiKey }} />
        </div>
      </SignedIn>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
    </>
  );
};
