function StatusListHeader() {
  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center justify-between pt-4 pb-1 pl-4 pr-2">
        <h3 className="text-xl font-semibold text-zinc-200">Status</h3>
      </div>

      <div className="flex gap-3 px-3 py-3 mx-2 rounded-md cursor-pointer hover:bg-neutral-800">
        <div className="overflow-hidden rounded-full w-11">
          <img
            src="https://usatodayhss.com/wp-content/uploads/sites/96/2022/08/11268798.jpeg?w=1000&h=600&crop=1"
            alt=""
            className="object-cover size-full"
          />
        </div>
        <div className="space-y-1">
          <h4 className="text-sm font-semibold text-zinc-200">My Status</h4>
          <h4 className="text-sm text-zinc-400">No update</h4>
        </div>
      </div>
    </div>
  );
}

export default StatusListHeader;
