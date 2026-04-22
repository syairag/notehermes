"use client";

import type { Task } from "@/types/task";

const priorityLabels: Record<Task["priority"], { label: string; color: string }> = {
  high: { label: "高", color: "bg-red-100 text-red-600" },
  medium: { label: "中", color: "bg-amber-100 text-amber-700" },
  low: { label: "低", color: "bg-green-100 text-green-700" },
};

interface TaskCardProps {
  task: Task;
  onMove: (id: string, status: Task["status"]) => void;
  onDelete: (id: string) => void;
}

export default function TaskCard({ task, onMove, onDelete }: TaskCardProps) {
  const priority = priorityLabels[task.priority];

  return (
    <div className="group bg-[#f7f7f5] hover:bg-white border border-[#e9e9e7] hover:border-[#d4d4d2] hover:shadow-sm rounded-md p-3 transition-all" style={{ fontFamily: "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" }}>
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-start gap-2 flex-1">
          {/* Checkbox */}
          <button
            onClick={() => onMove(task.id, task.status === "done" ? "todo" : "done")}
            className={`mt-0.5 shrink-0 w-4 h-4 rounded border flex items-center justify-center transition-colors ${
              task.status === "done"
                ? "bg-[#1d1d1f] border-[#1d1d1f]"
                : "border-[#d4d4d2] hover:border-[#9b9b9b]"
            }`}
          >
            {task.status === "done" && (
              <svg className="w-2.5 h-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            )}
          </button>
          <div className="flex-1 min-w-0">
            <h4 className={`text-sm leading-tight ${task.status === "done" ? "text-[#9b9b9b] line-through" : "text-[#1d1d1f]"}`}>
              {task.title}
            </h4>
            {task.description && (
              <p className="text-xs text-[#9b9b9b] mt-0.5 line-clamp-2">{task.description}</p>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
          {/* Move buttons */}
          {task.status !== "todo" && (
            <button onClick={() => onMove(task.id, task.status === "done" ? "doing" : "todo")} className="text-[#d4d4d2] hover:text-[#1d1d1f] p-0.5 transition-colors" title="左移">
              <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" /></svg>
            </button>
          )}
          {task.status !== "done" && (
            <button onClick={() => onMove(task.id, task.status === "todo" ? "doing" : "done")} className="text-[#d4d4d2] hover:text-[#1d1d1f] p-0.5 transition-colors" title="右移">
              <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" /></svg>
            </button>
          )}
          {/* Delete */}
          <button onClick={() => onDelete(task.id)} className="text-[#d4d4d2] hover:text-red-500 p-0.5 transition-colors" title="删除">
            <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
      </div>

      {/* Footer */}
      <div className="flex items-center gap-2 mt-2">
        <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${priority.color}`}>{priority.label}</span>
      </div>
    </div>
  );
}
