import { PhoneIncomingIcon, PhoneOutgoingIcon } from "lucide-react";

function CallListItem({ name, timestamp, callType, profile }) {
  const isMissedCall = callType === "missed";

  return (
    <div className="flex items-center gap-3 px-3 py-2 rounded-md cursor-pointer text-zinc-400 hover:bg-zinc-800">
      <div className="overflow-hidden rounded-full w-11 aspect-square shrink-0">
        <img
          src={profile}
          alt="Profile Image"
          className="object-cover size-full"
        />
      </div>
      <div className="flex-grow min-w-0 space-y-2">
        <div className="flex items-center justify-between">
          <h4 className="text-sm font-semibold text-zinc-200">{name}</h4>
          <span className="text-xs">{timestamp}</span>
        </div>
        <div
          className={`flex items-center gap-2 ${
            isMissedCall ? "text-red-300" : "text-neutral-400"
          }`}
        >
          {isMissedCall ? (
            <PhoneIncomingIcon size={14} />
          ) : (
            <PhoneOutgoingIcon size={14} />
          )}
          <span className="text-xs capitalize">{callType}</span>
        </div>
      </div>
    </div>
  );
}

export default CallListItem;
