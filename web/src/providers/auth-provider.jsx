import { createContext, useEffect, useState } from "react";

import { mutationApi } from "../hooks/useApi";
import {
  decryptData,
  encryptData,
  generateAndStoreKey,
} from "../utils/encryption";

export const AuthContext = createContext();

const TOKEN_KEY = "x-auth-token";
const USER_KEY = "x-auth-user";
const REFRESH_TOKEN_KEY = "x-refresh-token";

/**
 * @typedef User
 * @property {string} id - The user's id.
 * @property {string} username - The user's username.
 * @property {string} email - The user's email.
 * @property {string} profile_picture - The user's profile picture.
 */

/**
 * Stores the given auth data in local storage, encrypted with the given key.
 *
 * @param {CryptoKey} key The key to use for encryption.
 * @param {string} token The auth token to store.
 * @param {string} refreshToken The refresh token to store.
 * @param {User} user The user object to store.
 */
const storeEncryptedData = async (key, token, refreshToken, user) => {
  try {
    const encryptedToken = await encryptData(token, key);
    const encryptedRefreshToken = await encryptData(refreshToken, key);
    const encryptedUser = await encryptData(user, key);

    localStorage.setItem(TOKEN_KEY, JSON.stringify(encryptedToken));
    localStorage.setItem(
      REFRESH_TOKEN_KEY,
      JSON.stringify(encryptedRefreshToken)
    );
    localStorage.setItem(USER_KEY, JSON.stringify(encryptedUser));
  } catch (error) {
    console.log("Failed to encrypt data:", error);
    throw new Error("Encryption failed");
  }
};

/**
 * Retrieves the stored auth data from local storage and decrypts it with the given
 * encryption key.
 *
 * @param {CryptoKey} key The encryption key to use for decryption.
 * @returns {{ token: string, refreshToken: string, user: User } | null} The decrypted
 *   auth data if it exists, otherwise null.
 */
const retrieveDecryptedData = async (key) => {
  try {
    const storedToken = localStorage.getItem(TOKEN_KEY);
    const storedRefreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
    const storedUser = localStorage.getItem(USER_KEY);

    if (!storedToken || !storedRefreshToken || !storedUser) return null;

    const token = await decryptData(JSON.parse(storedToken), key);
    const refreshToken = await decryptData(JSON.parse(storedRefreshToken), key);
    const user = await decryptData(JSON.parse(storedUser), key);

    return { token, refreshToken, user };
  } catch (error) {
    console.error("Failed to decrypt data:", error);
    return null;
  }
};

/**
 * Provides the current user state and login/logout functions.
 *
 * This hook must be used within an AuthProvider. It will throw an error if used
 * outside of an AuthProvider.
 *
 * @returns {{ user: User | null, login: (formData: { email: string; password: string; }) => Promise<void>, logout: () => Promise<void> }}
 */
function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [refreshToken, setRefreshToken] = useState(null);
  const [key, setKey] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const init = async () => {
      try {
        const encryptionKey = await generateAndStoreKey();
        setKey(encryptionKey);

        const storedData = await retrieveDecryptedData(encryptionKey);
        if (storedData) {
          setToken(storedData.token);
          setRefreshToken(storedData.refreshToken);
          setUser(storedData.user);
        }

        setLoading(false);
      } catch (error) {
        console.log("Error during auth initialization:", error);
        setLoading(false);
      }
    };

    init();
  }, []);

  useEffect(() => {
    if (key && token && refreshToken && user) {
      storeEncryptedData(key, token, refreshToken, user).catch((error) => {
        console.log("Error storing encrypted data:", error);
      });
    }
  }, [key, token, refreshToken, user]);

  const login = async (formData) => {
    try {
      const result = await mutationApi("/auth/login", formData);

      if (result?.success) {
        setUser(result.data.user);
        setToken(result.data.token);
        setRefreshToken(result.data.refreshToken);

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
    setRefreshToken(null);

    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);

    window.location.replace("/auth/login");
  };

  const refreshAccessToken = async () => {
    try {
      const result = await mutationApi("/auth/refresh", { refreshToken });
      if (result?.success) {
        setToken(result.data.token);

        if (key && result.data.token) {
          const encryptedToken = await encryptData(result.data.token, key);
          localStorage.setItem(TOKEN_KEY, JSON.stringify(encryptedToken));
        }
      } else {
        console.log("Failed to refresh token:", result);
        logout();
      }
    } catch (error) {
      console.log("Failed to refresh access token:", error);
      logout();
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        refreshToken,
        login,
        logout,
        refreshAccessToken,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;
