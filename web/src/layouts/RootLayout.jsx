import { useEffect } from "react";
import { Outlet, useNavigate } from "react-router-dom";

import apiClient from "../api-client";
import Sidebar from "../components/Sidebar";

function RootLayout() {
  const navigate = useNavigate();

  useEffect(() => {
    apiClient.setLogoutCallback(() => {
      navigate("/auth/login", { replace: true });
    });
  }, [navigate]);

  return (
    <main className="relative flex h-screen overflow-hidden font-sans">
      <Sidebar />
      <Outlet />
    </main>
  );
}

export default RootLayout;
