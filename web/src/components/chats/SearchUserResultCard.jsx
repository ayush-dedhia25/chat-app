import {
  BadgeCheckIcon,
  CircleCheckBigIcon,
  CircleCheckIcon,
  MessageSquareTextIcon,
  SendHorizontalIcon,
} from "lucide-react";
import { Link } from "react-router-dom";

import { generateInitials } from "../../utils";
import apiClient from "../../api-client";

function SearchUserResultCard({ user }) {
  console.log("User:", user);

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
      case "request_received": {
        const acceptFriendRequest = async () => {
          try {
            const response = await apiClient.put(
              `/chats/requests/receive/${user?.request_id}`,
              {
                status: "accepted",
              }
            );
            console.log(response);
          } catch (error) {
            console.log(error);
          }
        };

        return (
          <button
            className="inline-flex items-center gap-2 px-2 py-2 text-sm rounded-md text-neutral-400 hover:bg-neutral-700/40"
            onClick={acceptFriendRequest}
          >
            Accept Request
            <CircleCheckIcon size={16} />
          </button>
        );
      }
      default: {
        const sendFriendRequest = async () => {
          try {
            const response = await apiClient.post("/chats/requests/send", {
              receiver_id: user.id,
            });
            console.log(response);
          } catch (error) {
            console.log(error);
          }
        };

        return (
          <button
            className="inline-flex items-center gap-2 px-2 py-2 text-xs border border-transparent rounded-md text-neutral-400 hover:bg-neutral-900/50 hover:border-neutral-700/60"
            onClick={sendFriendRequest}
          >
            Send Request
            <SendHorizontalIcon size={14} />
          </button>
        );
      }
    }
  };

  return (
    <div className="flex items-center gap-3 px-3 py-2 border rounded-md border-neutral-700">
      <div className="grid overflow-hidden rounded-full size-[38px] place-items-center bg-neutral-700">
        {user?.profile_picture ? (
          <img
            src={user?.profile_picture}
            alt={user?.name}
            className="object-cover size-full"
          />
        ) : (
          <span className="text-sm text-neutral-400">{generateInitials(user?.name)}</span>
        )}
      </div>
      <div className="flex-grow space-y-0.5">
        <h3 className="text-sm text-neutral-300">{user?.name}</h3>
        <h4 className="flex items-center gap-1.5 text-xs text-neutral-400">
          <span>@{user?.username}</span>{" "}
          {user?.isVerified && <BadgeCheckIcon size={12} />}
        </h4>
      </div>
      {renderResponseButton(user?.relationship_status)}
    </div>
  );
}

export default SearchUserResultCard;
