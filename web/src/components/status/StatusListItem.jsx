function StatusListItem({ name, timestamp, profile }) {
  return (
    <div className="flex gap-3 px-3 py-3 rounded-md cursor-pointer hover:bg-neutral-800">
      <div className="p-1 overflow-hidden border-[1.5px] border-green-400 rounded-full w-10">
        <img
          src={profile}
          alt=""
          className="object-cover rounded-full size-full"
        />
      </div>
      <div className="space-y-1">
        <h4 className="text-sm font-semibold text-zinc-200">{name}</h4>
        <h4 className="text-xs text-zinc-400">{timestamp}</h4>
      </div>
    </div>
  );
}

export default StatusListItem;
