import { useState, useEffect } from "react";

/**
 * @function useDebounce
 * @description Returns a debounced version of the given `value` after a `delay` in milliseconds.
 * @param {any} value The value to debounce.
 * @param {number} delay The delay in milliseconds to debounce the value.
 * @returns {any} The debounced value.
 * @example
 * const debouncedValue = useDebounce(value, 500);
 */
function useDebounce(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Clean up the timeout if value or delay changes
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

export default useDebounce;
