import { CornerRightDownIcon, Loader2Icon, XIcon } from "lucide-react";
import { useState } from "react";

import SearchUserResultCard from "../components/chats/SearchUserResultCard";
import useDebounce from "../hooks/useDebounce";
import useModal from "../hooks/useModal";
import useSearchUsers from "../hooks/useSearchUsers";

function SearchUserModal({ isOpen, onClose }) {
  const [searchTerm, setSearchTerm] = useState("");

  const modalRef = useModal(isOpen, onClose);
  const debouncedSearchTerm = useDebounce(searchTerm, 500);
  const { data, isLoading } = useSearchUsers(debouncedSearchTerm);

  const handleClose = () => {
    onClose();
  };

  return (
    <dialog
      ref={modalRef}
      className="z-50 overflow-hidden bg-transparent backdrop:bg-black/70 backdrop:backdrop-blur-[2px]"
      onClose={handleClose}
    >
      <div className="w-[80dvw] sm:w-[70dvw] md:w-[35dvw] bg-neutral-800 rounded-md border border-neutral-600">
        <header className="relative flex items-center justify-between gap-4 px-4 py-3 border-b border-neutral-700">
          <h3 className="text-sm font-semibold tracking-wider uppercase text-neutral-200">
            Search User
          </h3>
          <button
            className="box-border absolute p-2 rounded-full right-2 hover:bg-neutral-700/40 text-zinc-400"
            onClick={handleClose}
          >
            <XIcon size={20} />
            <span className="sr-only">Close</span>
          </button>
        </header>

        <div className="p-4">
          <input
            type="text"
            placeholder="Search by name or username"
            className="w-full p-2.5 px-3.5 text-sm bg-transparent border rounded-md border-neutral-700 text-neutral-300 placeholder:text-neutral-500 focus:ring-2 focus:ring-violet-400 focus:outline-none"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />

          <div className="mt-4">
            {isLoading ? (
              <p className="flex items-center justify-center gap-2 text-sm text-neutral-400">
                <Loader2Icon size={20} className="animate-spinner" />
                <span className="animate-pulser">Searching...</span>
              </p>
            ) : data === null ? (
              // Show this message when the user have not started to search for any user yet
              <p className="flex items-center justify-center gap-2 text-sm text-neutral-400">
                Start searching your friends
              </p>
            ) : data !== null && data?.results.length === 0 ? (
              // Show this message when no user found while trying to search for a user
              <p className="flex items-center justify-center gap-2 text-sm text-neutral-400">
                No user found! {`"${debouncedSearchTerm}"`}
              </p>
            ) : (
              <div>
                <h2 className="flex items-center gap-2 text-neutral-400">
                  Found {data?.results.length} Results <CornerRightDownIcon size={16} />
                </h2>

                <div className="flex flex-col gap-3 pr-2.5 mt-4 -mr-1.5 overflow-y-auto max-h-80">
                  {data?.results.map((user) => (
                    <SearchUserResultCard key={user.id} user={user} />
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </dialog>
  );
}

export default SearchUserModal;
