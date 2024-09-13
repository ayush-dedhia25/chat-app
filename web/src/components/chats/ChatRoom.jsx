import ChatRoomHeader from "./ChatRoomHeader";
import ChatRoomFooter from "./ChatRoomFooter";
import ChatBubble from "./ChatBubble";

const chats = [
  {
    messageId: "message-:1:",
    message: "Areee matlab hostel mai rehta hai na?",
    sender: "me",
    profile:
      "https://lh3.googleusercontent.com/a/ACg8ocIPxjTnlZsNm06dQt04knpW95GfiO3FMLv03WQzundKMJQ_Ouhy=s288-c-no",
  },
  {
    messageId: "message-:2:",
    message: "Ha",
    sender: "other",
    profile:
      "https://usatodayhss.com/wp-content/uploads/sites/96/2022/08/11268798.jpeg?w=1000&h=600&crop=1",
  },
  {
    messageId: "message-:3:",
    message:
      "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quae dolores unde, ab fugiat nostrum obcaecati.",
    sender: "other",
    profile:
      "https://usatodayhss.com/wp-content/uploads/sites/96/2022/08/11268798.jpeg?w=1000&h=600&crop=1",
  },
  {
    messageId: "message-:4:",
    message: "Okayy",
    sender: "me",
    profile:
      "https://lh3.googleusercontent.com/a/ACg8ocIPxjTnlZsNm06dQt04knpW95GfiO3FMLv03WQzundKMJQ_Ouhy=s288-c-no",
  },
  {
    messageId: "message-:5:",
    message: "Commit: Some Update",
    sender: "me",
    profile:
      "https://lh3.googleusercontent.com/a/ACg8ocIPxjTnlZsNm06dQt04knpW95GfiO3FMLv03WQzundKMJQ_Ouhy=s288-c-no",
  },
];

function ChatRoom() {
  return (
    <section className="flex flex-col w-full">
      {/* Chat header */}
      <ChatRoomHeader />

      {/* Chat body */}
      <div className="flex flex-col justify-end flex-1 gap-1 px-5 py-3 antialiased chat-room-body">
        {chats.map((chat, index, currentChats) => (
          <ChatBubble
            key={chat.messageId}
            message={chat.message}
            sender={chat.sender}
            previousMessage={index > 1 ? currentChats[index - 1] : null}
            profile={chat.profile}
          />
        ))}
      </div>

      {/* Chat footer */}
      <ChatRoomFooter />
    </section>
  );
}

export default ChatRoom;
