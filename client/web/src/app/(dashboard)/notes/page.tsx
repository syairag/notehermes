"use client";

import { useEffect, useState } from "react";
import { getNotes, type Note } from "@/lib/api";

const tagColors: Record<string, string> = {
  meeting: "bg-blue-100 text-blue-700",
  sprint: "bg-indigo-100 text-indigo-700",
  planning: "bg-cyan-100 text-cyan-700",
  research: "bg-purple-100 text-purple-700",
  AI: "bg-violet-100 text-violet-700",
  benchmarks: "bg-fuchsia-100 text-fuchsia-700",
  architecture: "bg-green-100 text-green-700",
  backend: "bg-emerald-100 text-emerald-700",
  design: "bg-teal-100 text-teal-700",
  frontend: "bg-amber-100 text-amber-700",
  UI: "bg-orange-100 text-orange-700",
  components: "bg-yellow-100 text-yellow-700",
  feedback: "bg-pink-100 text-pink-700",
  "user-research": "bg-rose-100 text-rose-700",
  devops: "bg-red-100 text-red-700",
  deployment: "bg-orange-100 text-orange-700",
};

const noteColors = [
  "border-l-blue-500",
  "border-l-purple-500",
  "border-l-green-500",
  "border-l-amber-500",
  "border-l-pink-500",
  "border-l-red-500",
  "border-l-teal-500",
  "border-l-indigo-500",
];

export default function NotesPage() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getNotes()
      .then((data) => {
        setNotes(data);
        setError(null);
      })
      .catch((err) => {
        console.error("Failed to fetch notes:", err);
        setError("Failed to load notes");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">📝 Notes</h1>
        <p className="text-sm text-gray-500 mt-1">
          Your smart notebook with AI search
        </p>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="flex items-center justify-center py-12">
          <p className="text-gray-500">Loading...</p>
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-center">
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && notes.length === 0 && (
        <div className="bg-white border border-gray-200 rounded-xl shadow-sm p-8 text-center">
          <p className="text-gray-500">No Notes</p>
        </div>
      )}

      {/* Notes Grid */}
      {!loading && !error && notes.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {notes.map((note, index) => (
            <div
              key={note.id}
              className={`bg-white border border-gray-200 border-l-4 ${noteColors[index % noteColors.length]} rounded-xl shadow-sm hover:shadow-md transition-shadow p-5 cursor-pointer`}
            >
              {/* Title & Date */}
              <div className="flex items-start justify-between gap-2 mb-3">
                <h3 className="text-sm font-bold text-gray-900 leading-tight">
                  {note.title}
                </h3>
                <span className="text-[11px] text-gray-400 whitespace-nowrap">
                  {note.date}
                </span>
              </div>

              {/* Content Snippet */}
              <p className="text-xs text-gray-500 leading-relaxed line-clamp-3 mb-4">
                {note.content}
              </p>

              {/* Tags */}
              <div className="flex flex-wrap gap-1.5">
                {note.tags.map((tag) => (
                  <span
                    key={tag}
                    className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${tagColors[tag] ?? "bg-gray-100 text-gray-600"}`}
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
