import {
  FileQuestionMark,
  House,
  IndianRupee,
  LogOut,
  Notebook,
  Settings,
  Users,
} from "lucide-react";
import { useState } from "react";

const Sidebar = () => {
  const [active, setActive] = useState("Dashboard");

  const navLinks = [
    { title: "Dashboard", icon: <House size={18} /> },
    { title: "My Courses", icon: <Notebook size={18} /> },
    { title: "Fees", icon: <IndianRupee size={18} /> },
    { title: "Community", icon: <Users size={18} /> },
    { title: "Settings", icon: <Settings size={18} /> },
    { title: "Help & Information", icon: <FileQuestionMark size={18} /> },
    { title: "Logout", icon: <LogOut size={18} /> },
  ];

  const activeIndex = navLinks.findIndex((item) => item.title === active);

  return (
    <aside className="h-full max-w-[15%] p-6 flex flex-col justify-between">
      {/* Top Section */}
      <div>
        <header className="flex items-center gap-1">
          <img src="/logo_dark.png" alt="logo" className="size-7" />
          <h1 className="text-2xl font-semibold font-heading">Eduverse</h1>
        </header>

        {/* Nav */}
        <nav className="mt-20">
          <ul className="relative space-y-5">
            {/* Sliding Bar for Top Menu */}
            {activeIndex < 5 && (
              <span
                className="absolute -right-6 w-1 h-8 bg-[#e63a54] rounded-full transition-all duration-300 ease-in-out"
                style={{
                  transform: `translateY(${activeIndex * 52}px)`,
                }}
              />
            )}

            {navLinks.slice(0, 5).map((item, idx) => (
              <li key={idx}>
                <button
                  onClick={() => setActive(item.title)}
                  className={`w-full flex items-center gap-2 text-left py-1 transition-all duration-200 cursor-pointer ${
                    active === item.title
                      ? "text-black font-medium"
                      : "text-neutral-400 hover:text-black"
                  }`}
                >
                  <span>{item.icon}</span>
                  <span>{item.title}</span>
                </button>
              </li>
            ))}
          </ul>
        </nav>
      </div>

      {/* Bottom Section */}
      <div className="w-full relative">
        <ul className="relative space-y-5">
          {/* Sliding Bar for Bottom Menu */}
          {activeIndex >= 5 && (
            <span
              className="absolute left -right-6 w-1 h-8 bg-[#e63a54] rounded-full transition-all duration-300 ease-in-out"
              style={{
                transform: `translateY(${(activeIndex - 5) * 52}px)`,
              }}
            />
          )}

          {navLinks.slice(5).map((item, idx) => (
            <li key={idx + 5}>
              <button
                onClick={() => setActive(item.title)}
                className={`w-full flex items-center gap-2 text-left py-1 transition-all duration-200 cursor-pointer ${
                  active === item.title
                    ? "text-black font-medium"
                    : "text-neutral-400 hover:text-black"
                }`}
              >
                <span>{item.icon}</span>
                <span>{item.title}</span>
              </button>
            </li>
          ))}
        </ul>
      </div>
    </aside>
  );
};

export default Sidebar;