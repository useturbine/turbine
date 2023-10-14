import { createBrowserRouter } from "react-router-dom";
import { Root } from "./routes/root";
import { ErrorPage } from "./error-page";
import { Home } from "./routes/home";
import { SignInPage } from "./routes/sign-in";
import { SignUpPage } from "./routes/sign-up";
import { Keys } from "./routes/keys";
import { Pipeline } from "./routes/pipeline";
import { CreatePipelinePage } from "./routes/create-pipeline";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "/",
        element: <Home />,
        errorElement: <ErrorPage />,
      },
      {
        path: "/create-pipeline",
        element: <CreatePipelinePage />,
      },
      {
        path: "/keys",
        element: <Keys />,
        errorElement: <ErrorPage />,
      },
      // {
      //   path: "/pipelines/:pipelineId",
      //   element: <Pipeline />,
      // },
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
