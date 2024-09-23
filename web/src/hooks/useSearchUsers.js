import { useEffect, useRef, useState } from "react";

import apiClient from "../api-client";

const useSearchUsers = (searchTerm) => {
  const [searchedResults, setSearchResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const cancelTokenRef = useRef(null);

  useEffect(() => {
    if (searchTerm) {
      const fetchMatchingUsers = async () => {
        // Cancel the previous request if it exists
        if (cancelTokenRef.current) {
          cancelTokenRef.current.cancel("Operation canceled due to new request.");
        }

        // Generate a new cancel token for the current request
        const source = apiClient.generateCancelToken();
        cancelTokenRef.current = source;

        setIsLoading(true);
        setError(null); // Reset error before making the new request

        try {
          const { data: response } = await apiClient.get(`/users?query=${searchTerm}`, {
            cancelToken: source.token,
          });
          setSearchResults(response?.data);
          setIsLoading(false);
        } catch (error) {
          setIsLoading(false);
          if (apiClient.isCancel(error)) {
            console.log("Request canceled:", error.message);
          } else {
            setError(error);
            console.log("Error:", error);
          }
        }
      };
      fetchMatchingUsers();
    } else {
      setSearchResults(null);
    }
  }, [searchTerm]);

  return { data: searchedResults, isLoading, error };
};

export default useSearchUsers;
