import {
  ArchiveIcon,
  BotIcon,
  ChevronsRightIcon,
  CircleDotDashed,
  CogIcon,
  MessageCircleMoreIcon,
  PhoneIcon,
  StarIcon,
} from "lucide-react";
import { useState } from "react";
import { NavLink } from "react-router-dom";

function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(true);

  return (
    <aside
      id="sidebar"
      className={`bg-neutral-700 flex flex-col px-1.5 py-3 gap-2 transition-[width] ease-in-out
        ${isCollapsed ? "w-[50px]" : "w-[190px]"}`}
    >
      <button
        className="inline-block p-2 rounded hover:bg-neutral-600 text-zinc-300"
        onClick={() => setIsCollapsed((prev) => !prev)}
      >
        <ChevronsRightIcon size={20} />
      </button>

      <div className="flex flex-col gap-2 overflow-hidden text-zinc-300">
        <NavLink
          to={"/chats"}
          className={({ isActive }) =>
            `flex items-center gap-3 p-2 text-sm rounded hover:bg-neutral-600 text-nowrap nav-item ${
              isActive && "active bg-neutral-600"
            }`
          }
        >
          <MessageCircleMoreIcon size={20} className="shrink-0" />
          Chats
        </NavLink>
        <NavLink
          to={"/calls"}
          className={({ isActive }) =>
            `flex items-center gap-3 p-2 text-sm rounded hover:bg-neutral-600 text-nowrap nav-item ${
              isActive && "active bg-neutral-600"
            }`
          }
        >
          <PhoneIcon size={20} className="shrink-0" />
          Calls
        </NavLink>
        <NavLink
          to={"/status"}
          className={({ isActive }) =>
            `flex items-center gap-3 p-2 text-sm rounded hover:bg-neutral-600 text-nowrap nav-item ${
              isActive && "active bg-neutral-600"
            }`
          }
        >
          <CircleDotDashed size={20} className="shrink-0" />
          Status
        </NavLink>
      </div>

      <div className="flex flex-col border-y-[2px] overflow-hidden border-neutral-600 py-2 gap-1 flex-1 text-zinc-300">
        <NavLink
          to={"/ask-ai"}
          className={({ isActive }) =>
            `flex items-center gap-3 p-2 text-sm rounded hover:bg-neutral-600 text-nowrap nav-item ${
              isActive && "active bg-neutral-600"
            }`
          }
        >
          <BotIcon size={20} className="shrink-0" />
          Ask AI
        </NavLink>
        <NavLink
          to={"/starred-messages"}
          className={({ isActive }) =>
            `flex items-center gap-3 p-2 text-sm rounded hover:bg-neutral-600 text-nowrap mt-auto nav-item ${
              isActive && "active bg-neutral-600"
            }`
          }
        >
          <StarIcon size={20} className="shrink-0" />
          Starred Messages
        </NavLink>
        <NavLink
          to={"/archived-chats"}
          className={({ isActive }) =>
            `flex items-center gap-3 p-2 text-sm rounded hover:bg-neutral-600 text-nowrap nav-item ${
              isActive && "active bg-neutral-600"
            }`
          }
        >
          <ArchiveIcon size={20} className="shrink-0" />
          Archived Chats
        </NavLink>
      </div>

      <div className="flex flex-col gap-3 overflow-hidden text-zinc-300">
        <NavLink
          to={"/settings"}
          className={({ isActive }) =>
            `flex items-center gap-3 p-2 text-sm rounded hover:bg-neutral-600 text-nowrap nav-item ${
              isActive && "active bg-neutral-600"
            }`
          }
        >
          <CogIcon size={22} className="shrink-0" />
          Settings
        </NavLink>
        <NavLink
          to={"/profile"}
          className="flex items-center gap-3 px-2 text-sm"
        >
          <div className="size-6 shrink-0">
            <img
              src="https://lh3.googleusercontent.com/a/ACg8ocIPxjTnlZsNm06dQt04knpW95GfiO3FMLv03WQzundKMJQ_Ouhy=s288-c-no"
              alt="User Profile"
              className="object-cover rounded-full size-full"
            />
          </div>
          Profile
        </NavLink>
      </div>
    </aside>
  );
}

export default Sidebar;
