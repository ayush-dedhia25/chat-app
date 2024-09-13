function ChatListItem() {
  return (
    <div className="text-zinc-400 flex gap-3 hover:bg-zinc-800 py-3 px-3 rounded-md cursor-pointer items-center">
      <div className="w-11 overflow-hidden rounded-full aspect-square shrink-0">
        <img
          src="https://usatodayhss.com/wp-content/uploads/sites/96/2022/08/11268798.jpeg?w=1000&h=600&crop=1"
          alt="Profile Image"
          className="size-full object-cover"
        />
      </div>
      <div className="flex-grow min-w-0">
        <div className="flex justify-between items-center">
          <h4 className="font-semibold text-zinc-200 text-sm">Ayush</h4>
          <span className="text-xs">21:44</span>
        </div>
        <p className="text-sm mt-1 truncate">
          Lorem ipsum dolor sit amet consectetur adipisicing.
        </p>
      </div>
    </div>
  );
}

export default ChatListItem;
