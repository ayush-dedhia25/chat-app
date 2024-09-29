import { useState } from "react";
import { useParams } from "react-router-dom";

import ChatList from "../components/chats/ChatList";
import ChatRoom from "../components/chats/ChatRoom";
import { useQueryApi } from "../hooks/useApi";
import SearchUserModal from "../modals/search-user-modal";

function Chats() {
  const { chatId } = useParams();
  const { result: conversations, isLoading: isLoadingConversations } =
    useQueryApi("/chats");

  const [isOpen, setIsOpen] = useState(false);

  const handleCloseModal = () => {
    setIsOpen(false);
  };

  return (
    <main className="flex flex-1">
      <ChatList
        conversations={conversations}
        isLoading={isLoadingConversations}
        openUserModal={() => setIsOpen(true)}
      />
      <ChatRoom chatId={chatId} />
      <SearchUserModal isOpen={isOpen} onClose={handleCloseModal} />
    </main>
  );
}

export default Chats;
