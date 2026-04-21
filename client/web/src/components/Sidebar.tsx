"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/inbox", label: "Inbox", icon: "📧" },
  { href: "/notes", label: "Notes", icon: "📝" },
  { href: "/tasks", label: "Tasks", icon: "✅" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 min-h-screen bg-gray-900 text-white flex flex-col shrink-0">
      {/* Logo */}
      <div className="px-6 py-6 border-b border-gray-700">
        <h1 className="text-xl font-bold tracking-tight">NoteHermes 🤖</h1>
        <p className="text-xs text-gray-400 mt-1">AI Smart Workspace</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? "bg-blue-600 text-white shadow"
                  : "text-gray-300 hover:bg-gray-800 hover:text-white"
              }`}
            >
              <span className="text-base">{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="px-4 py-4 border-t border-gray-700">
        <p className="text-xs text-gray-500">NoteHermes v0.1</p>
      </div>
    </aside>
  );
}
