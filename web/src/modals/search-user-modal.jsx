import { CornerRightDownIcon, XIcon } from "lucide-react";

import SearchUserResultCard from "../components/chats/SearchUserResultCard";
import useModal from "../hooks/useModal";

function SearchUserModal({ isOpen, onClose }) {
  const modalRef = useModal(isOpen, onClose);

  const handleClose = () => {
    onClose();
  };

  return (
    <dialog
      ref={modalRef}
      className="z-50 overflow-hidden bg-transparent backdrop:bg-black/70 backdrop:backdrop-blur-[2px]"
      onClose={handleClose}
    >
      <div className="w-[35dvw] bg-neutral-800 rounded-md border border-neutral-600">
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
          />

          <div className="mt-4">
            {/* <p className="flex items-center justify-center gap-2 text-sm text-neutral-400">
              <Loader2Icon size={20} className="animate-spinner" />
              <span className="animate-pulser">Searching...</span>
            </p> */}
            <div>
              <h2 className="flex items-center gap-2 text-neutral-400">
                Found 2 Results <CornerRightDownIcon size={16} />
              </h2>

              <div className="flex flex-col gap-3 pr-2.5 mt-4 -mr-1.5 overflow-y-auto max-h-80">
                <SearchUserResultCard
                  name="Ayush Dedhia"
                  username="d_ayush25"
                  profile="https://img.freepik.com/free-photo/love-illustrated-anime-style_23-2151103287.jpg"
                  isFriend
                  isVerified
                />
                <SearchUserResultCard
                  name="Jay Shah"
                  username="jayyy_shahh"
                  profile="https://m.media-amazon.com/images/I/81OcZThCE9L._AC_UF1000,1000_QL80_.jpg"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </dialog>
  );
}

export default SearchUserModal;
