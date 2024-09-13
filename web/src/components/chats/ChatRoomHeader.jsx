import { PhoneIcon, SearchIcon, VideoIcon } from "lucide-react";

function ChatRoomHeader() {
  return (
    <div className="flex items-center gap-3 pl-4 pr-2 py-2.5 bg-neutral-700">
      <div className="flex flex-grow gap-3">
        <div className="w-10 overflow-hidden rounded-full">
          <img
            src="https://usatodayhss.com/wp-content/uploads/sites/96/2022/08/11268798.jpeg?w=1000&h=600&crop=1"
            alt=""
            className="object-cover size-full"
          />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-zinc-200">Ayush Dedhia</h3>
          <p className="text-xs text-neutral-300 mt-0.5 tracking-wide">
            last seen today at 21:19
          </p>
        </div>
      </div>

      <div className="flex gap-2">
        <div className="flex h-10 overflow-hidden border rounded-md bg-neutral-600 border-neutral-500">
          <button className="px-3 hover:bg-neutral-800 text-zinc-400">
            <VideoIcon size={20} />
          </button>
          <span className="self-center w-[1px] bg-neutral-500 h-2/4" />
          <button className="px-3 hover:bg-neutral-800 text-zinc-400">
            <PhoneIcon size={18} />
          </button>
        </div>
        <button className="px-2.5 rounded-md hover:bg-neutral-600 text-zinc-400">
          <SearchIcon size={18} />
        </button>
      </div>
    </div>
  );
}

export default ChatRoomHeader;
