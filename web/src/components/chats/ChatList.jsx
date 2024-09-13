import ChatListHeader from "./ChatListHeader";
import ChatListItem from "./ChatListItem";

function ChatList() {
  return (
    <div className="flex flex-col w-[25%] bg-neutral-900">
      <ChatListHeader />

      <div className="flex-1 px-3 mt-6 mb-4 space-y-1 overflow-y-auto no-scrollbar">
        <ChatListItem />
        <ChatListItem />
        <ChatListItem />
      </div>
    </div>
  );
}

export default ChatList;
