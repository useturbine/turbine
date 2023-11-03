import { createBrowserRouter } from "react-router-dom";
import { Root } from "./routes/root";
import { ErrorPage } from "./error-page";
import { SignInPage } from "./routes/sign-in";
import { SignUpPage } from "./routes/sign-up";
import { Settings } from "./routes/settings";
import { CreateIndex } from "./routes/create-index";
import { Indexes } from "./routes/indexes";
import { Index } from "./routes/index";
import { ConnectDataSource } from "./routes/connect-data-source";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "/",
        element: <Indexes />,
        errorElement: <ErrorPage />,
      },
      {
        path: "/create-index",
        element: <CreateIndex />,
        errorElement: <ErrorPage />,
      },
      {
        path: "/settings",
        element: <Settings />,
        errorElement: <ErrorPage />,
      },
      {
        path: "/indexes/:indexId",
        element: <Index />,
        errorElement: <ErrorPage />,
      },
      {
        path: "/indexes/:indexId/connect-data-source",
        element: <ConnectDataSource />,
        errorElement: <ErrorPage />,
      },
    ],
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
