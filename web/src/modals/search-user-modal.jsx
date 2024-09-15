import { XIcon } from "lucide-react";

import useModal from "../hooks/useModal";

function SearchUserModal({ isOpen, onClose }) {
  const modalRef = useModal(isOpen);

  const handleClose = () => {
    onClose();
  };

  return (
    <dialog
      ref={modalRef}
      className="z-50 overflow-hidden bg-transparent backdrop:bg-black/70"
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
        </div>
      </div>
    </dialog>
  );
}

export default SearchUserModal;
