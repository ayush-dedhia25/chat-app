import { createBrowserRouter } from "react-router-dom";

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
      { path: "chats", element: <Chats /> },
      { path: "calls", element: <CallsPage /> },
      { path: "status", element: <StatusPage /> },
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
