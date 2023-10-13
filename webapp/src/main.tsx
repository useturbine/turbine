import React from "react";
import ReactDOM from "react-dom/client";
import "./main.css";
import { ClerkProvider } from "@clerk/clerk-react";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { Root } from "./routes/root";
import { ErrorPage } from "./error-page";
import { SignInPage } from "./routes/sign-in";
import { SignUpPage } from "./routes/sign-up";

const clerkPubKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/sign-in",
    element: <SignInPage />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/sign-up",
    element: <SignUpPage />,
    errorElement: <ErrorPage />,
  },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ClerkProvider
      publishableKey={clerkPubKey}
      signInUrl="/sign-in"
      signUpUrl="/sign-up"
    >
      <RouterProvider router={router} />
    </ClerkProvider>
  </React.StrictMode>
);
