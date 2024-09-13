import { ListFilterIcon, SearchIcon } from "lucide-react";

function ChatListHeader() {
  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center justify-between pl-4 pr-2 py-2">
        <h3 className="text-zinc-400 font-semibold text-xl">Chats</h3>
        <button className="text-zinc-400 px-2 py-2 hover:bg-neutral-800 rounded-md">
          <ListFilterIcon size={18} />
        </button>
      </div>

      <div className="flex items-center gap-2 bg-neutral-800 mx-4 p-2 rounded border-b border-zinc-200">
        <SearchIcon size={16} className="text-zinc-400" />
        <input
          type="text"
          placeholder="Search or start a new chat"
          className="bg-transparent text-sm focus:outline-none text-zinc-400 font-medium flex-grow"
        />
      </div>
    </div>
  );
}

export default ChatListHeader;
