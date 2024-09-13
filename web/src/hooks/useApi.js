import useSWR from "swr";

import apiClient from "../api-client";

const fetcher = (url) => apiClient(url).then((res) => res.data);

/**
 * Performs a GET request to the given URL and returns the response data.
 * Also returns a mutate function that can be used to revalidate the data.
 *
 * @param {string} url The URL to query.
 * @param {object} options Options to pass to useSWR.
 * @returns {object} An object with data, isLoading, isError, and mutate properties.
 *   isLoading is true if the data is currently being fetched, false otherwise.
 *   isError is true if there was an error fetching the data, false otherwise.
 *   mutate is a function that can be used to revalidate the data.
 */
export function useQueryApi(url, options = {}) {
  const { data, error, mutate } = useSWR(url, fetcher, {
    revalidateOnFocus: false,
    ...options,
  });

  return {
    data,
    isLoading: !error && !data,
    isError: error,
    mutate,
  };
}

/**
 * Performs a mutation request to the given URL with the given data and method.
 *
 * @param {string} url The URL to query.
 * @param {unknown} [data] The data to send with the request.
 * @param {string} [method="POST"] The HTTP method to use.
 * @returns {Promise<object>} A promise that resolves with the response data.
 * @throws {Error} If there is an error making the request.
 */
export async function mutationApi(url, data = null, method = "POST") {
  try {
    let response;

    switch (method.toUpperCase()) {
      case "POST":
        response = await apiClient.post(url, data);
        break;
      case "PUT":
        response = await apiClient.put(url, data);
        break;
      case "DELETE":
        response = await apiClient.delete(url);
        break;
      default:
        throw new Error(`Unsupported method: ${method}`);
    }

    return response.data;
  } catch (error) {
    console.log(`Error in ${method} request:`, error);
    throw error;
  }
}
