import { useCallback, useEffect, useRef } from "react";

/**
 * Manages the state of a modal dialog element.
 *
 * @param {boolean} isOpen Whether the modal should be open or not.
 * @returns {React.RefObject<HTMLDialogElement>} The `ref` to be passed to the modal dialog element.
 */
const useModal = (isOpen, onClose) => {
  const dialogRef = useRef(null);

  const handleBackdropClick = useCallback(
    (event) => {
      const dialogDimensions = dialogRef.current.getBoundingClientRect();
      if (
        event.clientX < dialogDimensions.left ||
        event.clientX > dialogDimensions.right ||
        event.clientY < dialogDimensions.top ||
        event.clientY > dialogDimensions.bottom
      ) {
        onClose();
      }
    },
    [onClose]
  );

  useEffect(() => {
    const dialog = dialogRef.current;

    if (isOpen) {
      dialog.showModal();
      document.body.style.overflow = "hidden";
      dialog.addEventListener("click", handleBackdropClick);
    } else {
      dialog.close();
      document.body.style.overflow = "unset";
    }

    const handleCancel = (event) => {
      event.preventDefault();
      onClose();
    };

    dialog.addEventListener("cancel", handleCancel);

    return () => {
      document.body.style.overflow = "unset";
      dialog.removeEventListener("click", handleBackdropClick);
      dialog.removeEventListener("cancel", handleCancel);
    };
  }, [handleBackdropClick, isOpen, onClose]);

  return dialogRef;
};

export default useModal;
