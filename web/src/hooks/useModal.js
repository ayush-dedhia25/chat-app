import { useEffect, useRef } from "react";

/**
 * Manages the state of a modal dialog element.
 *
 * @param {boolean} isOpen Whether the modal should be open or not.
 * @returns {React.RefObject<HTMLDialogElement>} The `ref` to be passed to the modal dialog element.
 */
const useModal = (isOpen) => {
  const dialogRef = useRef(null);

  useEffect(() => {
    const dialog = dialogRef.current;

    if (isOpen) {
      dialog.showModal();
      document.body.style.overflow = "hidden";
    } else {
      dialog.close();
      document.body.style.overflow = "unset";
    }

    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isOpen]);

  return dialogRef;
};

export default useModal;
