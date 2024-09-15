import { ListFilterIcon, SearchIcon } from "lucide-react";

function ChatListHeader() {
  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center justify-between py-2 pl-4 pr-2">
        <h3 className="text-xl font-semibold text-zinc-400">Chats</h3>
        <button className="px-2 py-2 rounded-md text-zinc-400 hover:bg-neutral-800">
          <ListFilterIcon size={18} />
        </button>
      </div>

      <div className="flex items-center gap-2 p-2 mx-4 border-b rounded bg-neutral-800 border-zinc-200">
        <SearchIcon size={16} className="text-zinc-400" />
        <input
          type="text"
          placeholder="Search or start a new chat"
          className="flex-grow text-sm font-medium bg-transparent focus:outline-none text-zinc-400"
        />
      </div>
    </div>
  );
}

export default ChatListHeader;
