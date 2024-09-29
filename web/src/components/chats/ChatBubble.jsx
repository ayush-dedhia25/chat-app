import useAuth from "@/hooks/useAuth";
import { generateInitials } from "@/utils";

function ChatBubble({ message, previousMessage }) {
  const { user } = useAuth();

  console.log({ message, previousMessage });

  const isSameBatch = previousMessage?.sender?.id === message?.sender?.id;
  const isSenderMe = message.sender.id === user?.id;
  const isFirstInBatch = !isSameBatch;

  const logicClasses = [
    isSenderMe ? "ml-auto from-me-subsequent-message" : "",
    isFirstInBatch ? (isSenderMe ? "from-me" : "from-other") : "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div className={`flex items-start gap-4 ${isSenderMe ? "flex-row-reverse" : ""}`}>
      <div
        className={`rounded-full overflow-hidden size-8 grid place-items-center ${
          isFirstInBatch ? "bg-neutral-400" : "invisible"
        }`}
      >
        {message.sender.profile_picture ? (
          <img
            src={message.sender.profile_picture}
            alt={`${message.sender.name} profile picture`}
            className="object-cover size-full"
          />
        ) : (
          <span className="text-sm font-semibold text-neutral-800">
            {generateInitials(message.sender.name)}
          </span>
        )}
      </div>
      <div className={`text-zinc-200 chat-bubble ${logicClasses}`}>
        <p className="text-sm text-black message">{message?.content}</p>
      </div>
    </div>
  );
}

export default ChatBubble;
