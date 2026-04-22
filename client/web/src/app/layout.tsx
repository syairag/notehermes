import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NoteHermes",
  description: "AI 驱动的智能工作台",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body style={{ fontFamily: "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', 'Noto Sans SC', sans-serif" }}>{children}</body>
    </html>
  );
}
