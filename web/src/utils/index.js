import clsx from "clsx";
import { twMerge } from "tw-merge";

export const cn = (...classNames) => twMerge(clsx(...classNames));
