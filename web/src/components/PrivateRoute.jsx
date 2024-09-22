import { Navigate } from "react-router-dom";

import useAuth from "../hooks/useAuth";

function PrivateRoute({ children }) {
  const { token, loading } = useAuth();

  if (loading) {
    return (
      <div className="absolute inset-0 grid place-items-center">
        <h1 className="text-neutral-400">Loading, please wait...</h1>
      </div>
    );
  }

  return token ? children : <Navigate to="/auth/login" />;
}

export default PrivateRoute;
