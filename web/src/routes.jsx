import { createBrowserRouter } from "react-router-dom";

import PrivateRoute from "./components/PrivateRoute";
import AuthLayout from "./layouts/AuthLayout";
import RootLayout from "./layouts/RootLayout";
import LoginPage from "./pages/auth/login";
import SignupPage from "./pages/auth/signup";
import CallsPage from "./pages/calls";
import Chats from "./pages/chats";
import StatusPage from "./pages/status";

export const routes = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      {
        path: "chats/:chatId",
        element: (
          <PrivateRoute>
            <Chats />
          </PrivateRoute>
        ),
      },
      {
        path: "calls",
        element: (
          <PrivateRoute>
            <CallsPage />
          </PrivateRoute>
        ),
      },
      {
        path: "status",
        element: (
          <PrivateRoute>
            <StatusPage />
          </PrivateRoute>
        ),
      },
    ],
  },
  {
    path: "/auth",
    element: <AuthLayout />,
    children: [
      { path: "login", element: <LoginPage /> },
      { path: "sign-up", element: <SignupPage /> },
    ],
  },
]);
