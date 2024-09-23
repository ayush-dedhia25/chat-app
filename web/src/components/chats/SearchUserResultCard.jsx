import {
  BadgeCheckIcon,
  CircleCheckBigIcon,
  CircleCheckIcon,
  MessageSquareTextIcon,
  SendHorizontalIcon,
} from "lucide-react";
import { Link } from "react-router-dom";

import { generateInitials } from "../../utils";

const renderResponseButton = (friendStatus) => {
  switch (friendStatus) {
    case "friends":
      return (
        <Link className="inline-flex items-center gap-2 px-2 py-2 text-xs border border-transparent rounded-md text-neutral-400 hover:bg-neutral-900/50 hover:border-neutral-700/60">
          Chat
          <MessageSquareTextIcon size={16} strokeWidth={1.5} />
        </Link>
      );
    case "request_sent":
      return (
        <button className="inline-flex items-center gap-2 px-2 py-2 pl-2.5 text-sm rounded-md text-neutral-400 hover:bg-neutral-700/40">
          Request Sent
          <CircleCheckBigIcon size={15} />
        </button>
      );
    case "request_received":
      return (
        <Link className="inline-flex items-center gap-2 px-2 py-2 text-sm rounded-md text-neutral-400 hover:bg-neutral-700/40">
          Accept Request
          <CircleCheckIcon size={16} />
        </Link>
      );
    default:
      return (
        <button className="inline-flex items-center gap-2 px-2 py-2 text-xs border border-transparent rounded-md text-neutral-400 hover:bg-neutral-900/50 hover:border-neutral-700/60">
          Send Request
          <SendHorizontalIcon size={14} />
        </button>
      );
  }
};

function SearchUserResultCard({ name, profile, friendStatus, username, isVerified }) {
  return (
    <div className="flex items-center gap-3 px-3 py-2 border rounded-md border-neutral-700">
      <div className="grid overflow-hidden rounded-full size-[38px] place-items-center bg-neutral-700">
        {profile ? (
          <img src={profile} alt={name} className="object-cover size-full" />
        ) : (
          <span className="text-sm text-neutral-400">{generateInitials(name)}</span>
        )}
      </div>
      <div className="flex-grow space-y-0.5">
        <h3 className="text-sm text-neutral-300">{name}</h3>
        <h4 className="flex items-center gap-1.5 text-xs text-neutral-400">
          <span>@{username}</span> {isVerified && <BadgeCheckIcon size={12} />}
        </h4>
      </div>
      {renderResponseButton(friendStatus)}
    </div>
  );
}

export default SearchUserResultCard;
