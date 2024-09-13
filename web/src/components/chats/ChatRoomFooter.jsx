import { SendHorizontalIcon, SmilePlusIcon } from "lucide-react";

function ChatRoomFooter() {
  return (
    <div className="flex items-center gap-3 py-2 pl-3 pr-2 bg-neutral-700">
      <button className="px-2 py-2 rounded-md text-zinc-200 hover:bg-neutral-600">
        <SmilePlusIcon size={20} />
      </button>
      <input
        type="text"
        placeholder="Type a message"
        className="flex-grow py-2 text-sm bg-transparent focus:outline-none text-zinc-200 placeholder:text-neutral-400"
      />
      <button className="px-2 py-2 rounded-md text-zinc-200 hover:bg-neutral-600">
        <SendHorizontalIcon size={20} strokeWidth={1.5} />
      </button>
    </div>
  );
}

export default ChatRoomFooter;
