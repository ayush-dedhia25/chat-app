import clsx from "clsx";
import { twMerge } from "tw-merge";

export const cn = (...classNames) => twMerge(clsx(...classNames));

/**
 * Generate initials from a full name
 *
 * @param {string} name - The full name from which to generate initials
 * @returns {string} The generated initials (e.g., 'JD' for 'John Doe')
 */
export const generateInitials = (name) => {
  if (!name) return ""; // Return empty if no name is provided

  // Split the name into words, then filter out any empty strings (in case of extra spaces)
  const nameParts = name.trim().split(/\s+/);

  // Get the first letter of the first and last word, or just the first word if it's a single name
  const initials =
    nameParts.length === 1
      ? nameParts[0][0] // If single word, just take the first letter
      : nameParts[0][0] + nameParts[nameParts.length - 1][0]; // Take the first and last initial

  return initials.toUpperCase(); // Return the initials in uppercase
};
