import { useState } from "react";
import ChatList from "../components/chats/ChatList";
import ChatRoom from "../components/chats/ChatRoom";
import SearchUserModal from "../modals/search-user-modal";

function Chats() {
  const [isOpen, setIsOpen] = useState(false);

  const handleCloseModal = () => {
    setIsOpen(false);
  };

  return (
    <main className="flex flex-1">
      <ChatList openUserModal={() => setIsOpen(true)} />
      <ChatRoom />
      <SearchUserModal isOpen={isOpen} onClose={handleCloseModal} />
    </main>
  );
}

export default Chats;
