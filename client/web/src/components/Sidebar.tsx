"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/inbox", label: "收件箱", icon: "📬" },
  { href: "/notes", label: "笔记", icon: "📝" },
  { href: "/tasks", label: "任务", icon: "☑️" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 min-h-screen bg-[#f7f7f5] border-r border-[#e9e9e7] flex flex-col shrink-0" style={{ fontFamily: "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" }}>
      {/* Logo */}
      <div className="px-3 py-4 flex items-center gap-2">
        <div className="w-7 h-7 bg-[#1d1d1f] rounded flex items-center justify-center text-white text-xs font-bold">N</div>
        <div>
          <h1 className="text-sm font-semibold text-[#1d1d1f]">NoteHermes</h1>
          <p className="text-[10px] text-[#9b9b9b] leading-none">AI 智能工作台</p>
        </div>
      </div>

      <div className="h-px bg-[#e9e9e7] mx-3" />

      {/* Navigation */}
      <nav className="flex-1 px-1.5 py-2 space-y-0.5">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-2 px-2 py-1.5 rounded text-sm transition-colors ${
                isActive
                  ? "bg-[#e8e8e6] text-[#1d1d1f] font-medium"
                  : "text-[#5e5e5e] hover:bg-[#ebebeb] hover:text-[#1d1d1f]"
              }`}
            >
              <span className="text-base leading-none">{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="px-3 py-3 border-t border-[#e9e9e7]">
        <p className="text-[10px] text-[#9b9b9b]">NoteHermes v0.1</p>
      </div>
    </aside>
  );
}
