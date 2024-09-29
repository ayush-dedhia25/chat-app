import { useEffect } from "react";

import useAuth from "@/hooks/useAuth";
import { useQueryApi } from "../../hooks/useApi";
import ChatBubble from "./ChatBubble";
import ChatRoomFooter from "./ChatRoomFooter";
import ChatRoomHeader from "./ChatRoomHeader";

function ChatRoom({ chatId }) {
  const { socket } = useAuth();
  const { result, isLoading, refreshData } = useQueryApi(`/chats/${chatId}/messages`);

  useEffect(() => {
    if (socket) {
      socket.on("send-message:error", (error) => {
        console.log(error);
      });

      socket.on("new-message", (data) => {
        console.log("new-message-received:", data);
        refreshData(`/chats/${chatId}/messages`);
      });
    }

    return () => {
      if (socket) {
        socket.off("send-message:error");
        socket.off("new-message");
      }
    };
  }, [chatId, refreshData, socket]);

  const friend = result?.data?.friend; // data.friend
  const messages = result?.data?.messages; // data.messages

  if (isLoading) {
    return <div>Loading...</div>;
  }

  const handleSendMessage = (message) => {
    socket.emit("send-message", { chat_id: chatId, content: message });
  };

  return (
    <section className="flex flex-col w-full">
      {/* Chat header */}
      <ChatRoomHeader friend={friend} />

      {/* Chat body */}
      <div className="flex flex-col justify-end flex-1 gap-1 px-5 py-3 antialiased chat-room-body">
        {messages?.map((chat, index, currentChats) => (
          <ChatBubble
            key={chat.messageId}
            message={chat}
            previousMessage={index > 0 ? currentChats[index - 1] : null}
          />
        ))}
      </div>

      {/* Chat footer */}
      <ChatRoomFooter sendMessage={handleSendMessage} />
    </section>
  );
}

export default ChatRoom;
