"use client";

import { useEffect, useState } from "react";
import { getNotes, createNote, deleteNote, type Note } from "@/lib/api";

const noteColors = [
  "border-l-blue-400", "border-l-purple-400", "border-l-green-400",
  "border-l-amber-400", "border-l-pink-400", "border-l-red-400",
  "border-l-teal-400", "border-l-indigo-400",
];

const presetTags = ["会议", "计划", "调研", "AI", "架构", "后端", "前端", "设计", "运维", "部署"];

export default function NotesPage() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newContent, setNewContent] = useState("");
  const [newTags, setNewTags] = useState<string[]>([]);

  const loadNotes = () => {
    getNotes()
      .then((data) => { setNotes(data); setError(null); })
      .catch(() => { setError("笔记加载失败"); })
      .finally(() => setLoading(false));
  };

  useEffect(() => { loadNotes(); }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    try {
      await createNote({ title: newTitle.trim(), content: newContent.trim(), tags: newTags });
      setNewTitle(""); setNewContent(""); setNewTags([]); setShowForm(false);
      loadNotes();
    } catch { setError("创建失败"); }
  };

  const handleDelete = async (id: string) => {
    try { await deleteNote(id); loadNotes(); }
    catch { setError("删除失败"); }
  };

  const toggleTag = (tag: string) => {
    setNewTags(prev => prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]);
  };

  return (
    <div style={{ fontFamily: "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" }}>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <span className="text-3xl">📝</span>
          <div>
            <h1 className="text-[30px] font-semibold text-[#1d1d1f] leading-tight">笔记</h1>
            <p className="text-sm text-[#9b9b9b] mt-0.5">智能笔记本，支持 AI 搜索</p>
          </div>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-1.5 bg-[#1d1d1f] hover:bg-[#2d2d2f] text-white px-3.5 py-2 rounded-md text-sm font-medium transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
          </svg>
          新建
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="mb-4 bg-[#fef3f2] border border-[#fecdca] text-[#c22] px-4 py-3 rounded-lg text-sm">{error}</div>
      )}

      {/* New Note Form - Notion style */}
      {showForm && (
        <div className="mb-6 bg-[#f7f7f5] border border-[#e9e9e7] rounded-lg p-5">
          <input
            type="text"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            placeholder="笔记标题"
            className="w-full px-0 py-2 border-0 bg-transparent text-xl font-semibold text-[#1d1d1f] focus:outline-none placeholder:text-[#d4d4d2]"
            autoFocus
            required
          />
          <textarea
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
            placeholder="开始写作..."
            rows={5}
            className="w-full px-0 py-3 border-0 bg-transparent text-sm text-[#37352f] focus:outline-none resize-none placeholder:text-[#d4d4d2]"
          />
          {/* Tags */}
          <div className="flex flex-wrap gap-1.5 pb-3">
            {presetTags.map(tag => (
              <button key={tag} type="button" onClick={() => toggleTag(tag)}
                className={`text-[11px] px-2.5 py-1 rounded-md transition-colors ${newTags.includes(tag) ? "bg-[#1d1d1f] text-white" : "bg-[#e8e8e6] text-[#5e5e5e] hover:bg-[#e0e0de]"}`}>
                #{tag}
              </button>
            ))}
          </div>
          <div className="flex gap-2">
            <button type="submit" onClick={handleCreate} className="bg-[#1d1d1f] hover:bg-[#2d2d2f] text-white px-4 py-1.5 rounded-md text-sm font-medium transition-colors">
              保存
            </button>
            <button onClick={() => setShowForm(false)} className="text-[#5e5e5e] hover:text-[#1d1d1f] px-3 py-1.5 rounded-md text-sm transition-colors">
              取消
            </button>
          </div>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="flex items-center justify-center py-20">
          <div className="w-6 h-6 border-2 border-[#e9e9e7] border-t-[#1d1d1f] rounded-full animate-spin" />
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && notes.length === 0 && !showForm && (
        <div className="text-center py-20">
          <div className="text-5xl mb-4">📄</div>
          <p className="text-[#9b9b9b] text-base mb-1">还没有笔记</p>
          <button onClick={() => setShowForm(true)} className="text-[#1d1d1f] text-sm font-medium underline underline-offset-2 hover:opacity-70 transition-opacity">
            创建第一条笔记
          </button>
        </div>
      )}

      {/* Notes Grid - Notion style cards */}
      {!loading && !error && notes.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {notes.map((note, index) => (
            <div key={note.id} className={`group bg-[#f7f7f5] hover:bg-white border border-[#e9e9e7] hover:border-[#d4d4d2] hover:shadow-sm border-l-4 ${noteColors[index % noteColors.length]} rounded-md p-4 cursor-pointer transition-all`}>
              <div className="flex items-start justify-between gap-2 mb-2">
                <h3 className="text-sm font-semibold text-[#1d1d1f]">{note.title}</h3>
                <button onClick={() => handleDelete(note.id)} className="text-[#d4d4d2] hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100" title="删除">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <p className="text-xs text-[#5e5e5e] leading-relaxed line-clamp-3 mb-3">{note.content}</p>
              {note.tags.length > 0 && (
                <div className="flex flex-wrap gap-1">
                  {note.tags.map(tag => (
                    <span key={tag} className="text-[10px] px-1.5 py-0.5 bg-[#e8e8e6] text-[#5e5e5e] rounded">{tag}</span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
