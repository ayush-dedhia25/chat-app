import axios from "axios";
import {
  decryptData,
  encryptData,
  generateAndStoreKey,
} from "./utils/encryption";

class ApiClient {
  /**
   * Constructor for ApiClient
   *
   * @param {string} baseUrl Base URL for the API
   *
   * Initializes the API client with the given base URL and sets up interceptors
   * for handling authentication and refreshing the token when it expires.
   */
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

  /**
   * Sets up request and response interceptors for the axios instance.
   *
   * Request interceptors:
   * - `handleRequest`: adds the `Authorization` header with the access token
   * - `handleRequestError`: logs the error
   *
   * Response interceptors:
   * - `(response) => response`: passes the response through
   * - `handleResponseError`: handles the response error
   */
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

  /**
   * Add the auth token to the request headers if it exists
   *
   * @param {import("axios").AxiosRequestConfig} config
   * @returns {Promise<import("axios").AxiosRequestConfig>}
   */
  async handleRequest(config) {
    const encryptedToken = localStorage.getItem("x-auth-token");

    if (encryptedToken) {
      try {
        // Get the stored encryption key or generate one if its not available
        const encryptionKey = await generateAndStoreKey();

        // Decrypt the token
        const token = await decryptData(
          JSON.parse(encryptedToken),
          encryptionKey
        );

        // Add the decrypted token to the Authorization header
        config.headers["Authorization"] = `Bearer ${token}`;
      } catch (error) {
        console.log("Failed to decrypt token:", error);
      }
    }

    return config;
  }

  /**
   * Handles request errors by rejecting the promise with the error
   *
   * @param {Error} error
   * @returns {Promise<never>}
   */
  handleRequestError(error) {
    return Promise.reject(error);
  }

  /**
   * Handles response errors by retrying the request with a new auth token if a 401 is encountered
   *
   * @param {import("axios").AxiosError} error
   * @returns {Promise<import("axios").AxiosResponse<unknown>>}
   */
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

  /**
   * Retrieves a new access token by making a request to the server using the current refresh token
   *
   * @returns {Promise<string>} The new access token
   * @throws {Error} If the refresh token is not found or if the request to the server fails
   */
  async pleaseRefreshToken() {
    // Retrieve the encrypted refresh token from localStorage
    const encryptedRefreshToken = localStorage.getItem("x-refresh-token");

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
      localStorage.setItem("x-refresh-token", JSON.stringify(encryptedToken));
      return newToken;
    } catch (error) {
      console.error("Failed to refresh token:", error);
      throw error;
    }
  }

  /**
   * Called when a new auth token is obtained from the server. Subscribers are
   * notified and the refreshing flag is reset.
   *
   * @param {string} token The new auth token.
   */
  onRefreshSuccess(token) {
    this.refreshSubscribers.forEach((callback) => callback(token));
    this.refreshSubscribers = [];
    this.isRefreshing = false;
  }

  /**
   * Called when the request to refresh the auth token fails. The promise is
   * rejected with the error, the refreshing flag is reset, and the logout
   * method is called.
   *
   * @param {Error} error The error that occurred during the request.
   */
  onRefreshFailure(error) {
    this.refreshSubscribers = [];
    this.isRefreshing = false;
    console.error("Token refresh failed:", error);
    this.logout();
  }

  /**
   * Logs the user out by removing the auth token from local storage and calling
   * the logout callback if it's set.
   */
  logout() {
    localStorage.removeItem("authToken");
    if (this.onLogout) {
      this.onLogout();
    }
  }

  /**
   * Sets the logout callback to be called when the user logs out.
   *
   * @param {Function} callback The callback function to be called when the user logs out.
   * @returns {void}
   */
  setLogoutCallback(callback) {
    this.onLogout = callback;
  }

  /**
   * Makes a GET request to the given URL with the given config.
   *
   * @param {string} url The URL to make the request to.
   * @param {import("axios").AxiosRequestConfig} [config] The config to pass to the request.
   * @returns {Promise<import("axios").AxiosResponse<unknown>>} A promise that resolves with the response.
   */
  get(url, config) {
    return this.api.get(url, config);
  }

  /**
   * Makes a POST request to the given URL with the given config.
   *
   * @param {string} url The URL to make the request to.
   * @param {unknown} data The data to send with the request.
   * @param {import("axios").AxiosRequestConfig} [config] The config to pass to the request.
   * @returns {Promise<import("axios").AxiosResponse<unknown>>} A promise that resolves with the response.
   */
  post(url, data, config) {
    return this.api.post(url, data, config);
  }

  /**
   * Makes a PUT request to the given URL with the given config.
   *
   * @param {string} url The URL to make the request to.
   * @param {unknown} data The data to send with the request.
   * @param {import("axios").AxiosRequestConfig} [config] The config to pass to the request.
   * @returns {Promise<import("axios").AxiosResponse<unknown>>} A promise that resolves with the response.
   */
  put(url, data, config) {
    return this.api.put(url, data, config);
  }

  /**
   * Makes a DELETE request to the given URL with the given config.
   *
   * @param {string} url The URL to make the request to.
   * @param {import("axios").AxiosRequestConfig} [config] The config to pass to the request.
   * @returns {Promise<import("axios").AxiosResponse<unknown>>} A promise that resolves with the response.
   */
  delete(url, config) {
    return this.api.delete(url, config);
  }
}

export default new ApiClient(import.meta.env.VITE_API_URL);
