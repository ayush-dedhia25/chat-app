import clsx from "clsx";
import { twMerge } from "tw-merge";

export const cn = (...classNames) => twMerge(clsx(...classNames));

export const generateInitials = (name) => {
  if (!name) return "";
  const [firstName, lastName] = name.split(" ");
  return `${firstName[0]}${lastName[0]}`.toUpperCase();
};
