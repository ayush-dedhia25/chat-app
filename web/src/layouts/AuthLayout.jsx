import { Outlet } from "react-router-dom";

function AuthLayout() {
  return (
    <main className="flex h-screen">
      <Outlet />

      <div className="flex-1 py-4">
        <div className="flex flex-col items-center justify-center ml-auto mr-6 auth-image">
          <div className="flex flex-col items-center gap-2">
            <img
              src="/textify-logo.png"
              alt="Textify.in"
              className="object-contain w-48 mb-2"
            />
            <h2 className="text-4xl font-black tracking-wide text-violet-100">
              Textify.in
            </h2>
            <p className="px-3 py-1 italic text-white border rounded bg-zinc-300/25 border-zinc-400 backdrop-blur-[2px]">
              <q>Stay connected with those who matter, effortlessly.</q>
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}

export default AuthLayout;
