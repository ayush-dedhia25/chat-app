import ChatList from "../components/chats/ChatList";
import ChatRoom from "../components/chats/ChatRoom";

function Chats() {
  return (
    <main className="flex flex-1">
      <ChatList />
      {/* Main Chat Area */}
      <ChatRoom />
    </main>
  );
}

export default Chats;
