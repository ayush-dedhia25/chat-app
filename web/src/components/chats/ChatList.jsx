import { PlusIcon } from "lucide-react";

import ChatListHeader from "./ChatListHeader";
import ChatListItem from "./ChatListItem";

function ChatList({ conversations, isLoading, openUserModal }) {
  return (
    <div className="flex flex-col w-[30%] bg-neutral-900">
      <ChatListHeader />

      <div className="relative flex-1 px-3 mt-6 mb-4 space-y-1 overflow-y-auto no-scrollbar">
        {isLoading ? (
          "Fetching chats..."
        ) : conversations?.data?.length !== 0 ? (
          conversations?.data?.map((chat) => <ChatListItem key={chat.id} chat={chat} />)
        ) : (
          <div className="flex flex-col items-center w-full">
            <p className="p-3 text-sm italic text-center text-zinc-500">
              You have no active chats with anyone. Start by searching the people you want
              to chat with.
            </p>

            <button
              className="inline-flex items-center gap-1.5 px-3 py-2 text-sm rounded-md text-violet-400 bg-neutral-800 hover:bg-violet-500 hover:text-violet-100"
              onClick={openUserModal}
            >
              Start a new chat <PlusIcon size={16} />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatList;
