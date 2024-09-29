import useSWR from "swr";

import apiClient from "../api-client";

const fetcher = (url) => apiClient.get(url).then((res) => res.data);

/**
 * Fetches data from the given URL using the `apiClient` and provides the results
 * in a format similar to `react-query`'s `useQuery`.
 *
 * @param {string} url The URL to query.
 * @param {object} [options] Options to pass to `useSWR`.
 * @returns {object} An object with the following properties:
 *   - `result`: The data returned from the API.
 *   - `isLoading`: A boolean indicating whether the data is still being loaded.
 *   - `hasError`: A boolean indicating whether there was an error loading the data.
 *   - `error`: The error that occurred if `hasError` is true.
 *   - `refreshData`: A function to call to re-fetch the data from the API.
 */
export function useQueryApi(url, options = {}) {
  const { data, error, mutate } = useSWR(url, fetcher, {
    revalidateOnFocus: false,
    ...options,
  });

  return {
    result: data,
    isLoading: !error && !data,
    hasError: !!error,
    error,
    refreshData: mutate,
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
