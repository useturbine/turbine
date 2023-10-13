import {
  RedirectToSignIn,
  SignedIn,
  SignedOut,
  UserButton,
} from "@clerk/clerk-react";
import { Navbar } from "flowbite-react";
import { Link } from "react-router-dom";

export const Root = () => {
  return (
    <>
      <SignedIn>
        <Navbar fluid rounded>
          <Navbar.Brand as={Link} href="https://app.useturbine.com">
            <img
              src="/images/turbine.png"
              className="mr-3 h-6 sm:h-9"
              alt="Turbine Logo"
            />
            <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
              Turbine
            </span>
          </Navbar.Brand>
          <UserButton />
        </Navbar>
      </SignedIn>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
    </>
  );
};
