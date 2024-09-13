function ChatBubble({ message, sender, previousMessage, profile }) {
  const isSameBatch = previousMessage?.sender === sender;
  const isSenderMe = sender === "me";
  const isFirstInBatch = !isSameBatch;

  const logicClasses = [
    isSenderMe ? "ml-auto from-me-subsequent-message" : "",
    isFirstInBatch ? (isSenderMe ? "from-me" : "from-other") : "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div
      className={`flex items-start gap-4 ${
        isSenderMe ? "flex-row-reverse" : ""
      }`}
    >
      <div
        className={`rounded-full overflow-hidden size-8 ${
          isFirstInBatch ? "bg-neutral-400" : "invisible"
        }`}
      >
        <img src={profile} alt="" className="object-cover size-full" />
      </div>
      <div className={`text-zinc-200 chat-bubble ${logicClasses}`}>
        <p className="text-sm text-black message">{message}</p>
      </div>
    </div>
  );
}

export default ChatBubble;
