import axios from "axios";

import { decryptData, encryptData, generateAndStoreKey } from "./utils/encryption";
import { REFRESH_TOKEN_KEY, TOKEN_KEY } from "./constants";

class ApiClient {
  constructor(baseUrl) {
    this.api = axios.create({
      baseURL: baseUrl,
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },
    });

    this.isRefreshing = false;
    this.refreshSubscribers = [];
    this.setupInterceptors();
  }

  setupInterceptors() {
    this.api.interceptors.request.use(
      this.handleRequest.bind(this),
      this.handleRequestError.bind(this)
    );

    this.api.interceptors.response.use(
      (response) => response,
      this.handleResponseError.bind(this)
    );
  }

  async handleRequest(config) {
    const encryptedToken = localStorage.getItem(TOKEN_KEY);

    if (encryptedToken) {
      try {
        // Get the stored encryption key or generate one if its not available
        const encryptionKey = await generateAndStoreKey();

        // Decrypt the token
        const token = await decryptData(JSON.parse(encryptedToken), encryptionKey);

        // Add the decrypted token to the Authorization header
        config.headers["Authorization"] = `Bearer ${token}`;
      } catch (error) {
        console.log("Failed to decrypt token:", error);
      }
    }

    return config;
  }

  handleRequestError(error) {
    return Promise.reject(error);
  }

  async handleResponseError(error) {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (this.isRefreshing) {
        return new Promise((resolve) => {
          this.refreshSubscribers.push((token) => {
            originalRequest.headers["Authorization"] = `Bearer ${token}`;
            resolve(this.api(originalRequest));
          });
        });
      }

      originalRequest._retry = true;
      this.isRefreshing = true;

      try {
        const newToken = await this.pleaseRefreshToken();
        this.onRefreshSuccess(newToken);
        originalRequest.headers["Authorization"] = `Bearer ${newToken}`;
        return this.api(originalRequest);
      } catch (refreshError) {
        this.onRefreshFailure(refreshError);
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }

  async pleaseRefreshToken() {
    // Retrieve the encrypted refresh token from localStorage
    const encryptedRefreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);

    if (!encryptedRefreshToken) {
      throw new Error("Refresh token not found");
    }

    try {
      // Get the stored encryption key or generate one if it's not available
      const encryptionKey = await generateAndStoreKey();

      // Decrypt the refresh token
      const refreshToken = await decryptData(
        JSON.parse(encryptedRefreshToken),
        encryptionKey
      );

      // Make the request to the server to get a new access token using the decrypted refresh token
      const { data: response } = await axios.post("/auth/refresh", {
        refreshToken,
      });

      // Store the new access token (you can encrypt it before storing if needed)
      const newToken = response.data.token;
      const encryptedToken = await encryptData(newToken, encryptionKey);
      localStorage.setItem(REFRESH_TOKEN_KEY, JSON.stringify(encryptedToken));
      return newToken;
    } catch (error) {
      console.error("Failed to refresh token:", error);
      throw error;
    }
  }

  onRefreshSuccess(token) {
    this.refreshSubscribers.forEach((callback) => callback(token));
    this.refreshSubscribers = [];
    this.isRefreshing = false;
  }

  onRefreshFailure(error) {
    this.refreshSubscribers = [];
    this.isRefreshing = false;
    console.error("Token refresh failed:", error);
    this.logout();
  }

  logout() {
    localStorage.removeItem("authToken");
    if (this.onLogout) {
      this.onLogout();
    }
  }

  setLogoutCallback(callback) {
    this.onLogout = callback;
  }

  get(url, config) {
    return this.api.get(url, config);
  }

  post(url, data, config) {
    return this.api.post(url, data, config);
  }

  put(url, data, config) {
    return this.api.put(url, data, config);
  }

  delete(url, config) {
    return this.api.delete(url, config);
  }

  generateCancelToken() {
    return axios.CancelToken.source();
  }

  isCancel(error) {
    return axios.isCancel(error);
  }
}

export default new ApiClient(import.meta.env.VITE_API_URL);
