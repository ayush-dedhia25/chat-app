import { Link } from "react-router-dom";

import { generateInitials } from "../../utils";

function ChatListItem({ chat }) {
  console.log("chat", chat);

  return (
    <Link to={`/chats/${chat?.id}`}>
      <div className="flex items-center gap-3 px-3 py-3 rounded-md cursor-pointer text-zinc-400 hover:bg-zinc-800">
        <div className="grid overflow-hidden rounded-full w-11 aspect-square shrink-0 place-items-center bg-neutral-700">
          {chat?.members.profile_picture ? (
            <img
              src={chat?.members.profile_picture}
              alt={`${chat?.members.name} profile Image`}
              className="object-cover size-full"
            />
          ) : (
            <span className="text-sm font-semibold text-neutral-400">
              {generateInitials(chat?.members.name)}
            </span>
          )}
        </div>
        <div className="flex-grow min-w-0">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-semibold text-zinc-200">{chat?.members?.name}</h4>
            {chat?.last_message && (
              <span className="text-xs">
                {new Date(chat?.last_message?.sent_at).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </span>
            )}
          </div>
          <p className="mt-1 text-sm truncate">
            {chat?.last_message
              ? chat?.last_message?.content
              : "Click to start up a conversation"}
          </p>
        </div>
      </div>
    </Link>
  );
}

export default ChatListItem;
