import { createContext, useContext, useState } from "react";

import { mutationApi } from "../hooks/useApi";

const AuthContent = createContext();

/**
 * Provides the current user state and login/logout functions.
 *
 * This hook must be used within an AuthProvider. It will throw an error if used
 * outside of an AuthProvider.
 *
 * @returns {{ user: User | null, login: (formData: { email: string; password: string; }) => Promise<void>, logout: () => Promise<void> }}
 */
export const useAuth = () => {
  const context = useContext(AuthContent);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("authToken") || null);

  const login = async (formData) => {
    try {
      const result = await mutationApi("/auth/login", formData);
      if (result?.success) {
        setUser(result.data.user);
        setToken(result.data.token);
        localStorage.setItem("authToken", result.token);
        window.location.replace("/chats");
      }
    } catch (error) {
      if (error?.response) {
        console.log(error.response.data);
        if (error?.response?.status === 404) {
          console.log("User not found");
        }
      }
      console.log(error);
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("authToken");
    window.location.replace("/auth/login");
  };

  return (
    <AuthContent.Provider value={{ user, token, logout, login }}>
      {children}
    </AuthContent.Provider>
  );
}

export default AuthProvider;
