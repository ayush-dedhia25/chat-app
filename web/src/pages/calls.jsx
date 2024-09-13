import { LockIcon, MousePointerClickIcon } from "lucide-react";
import CallList from "../components/calls/CallList";

function CallsPage() {
  return (
    <main className="flex flex-1">
      <CallList />

      <section className="flex-1">
        <div className="flex flex-col items-center justify-center gap-6 size-full">
          <img
            src="/textify-logo.png"
            alt=""
            className="object-contain w-36 grayscale"
          />
          <div className="flex flex-col items-center gap-2">
            <h4 className="flex items-center gap-2 text-lg text-zinc-300">
              <MousePointerClickIcon size={24} /> Click on a contact to call
              them
            </h4>
            <p className="flex items-center gap-2 text-sm text-zinc-500">
              <LockIcon size={14} /> Calls are end-to-end encrypted
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}

export default CallsPage;
