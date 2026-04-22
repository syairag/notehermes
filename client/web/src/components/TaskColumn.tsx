"use client";

import type { Task } from "@/types/task";
import TaskCard from "./TaskCard";

interface TaskColumnProps {
  title: string;
  status: Task["status"];
  tasks: Task[];
  onMove: (id: string, status: Task["status"]) => void;
  onDelete: (id: string) => void;
}

export default function TaskColumn({ title, status, tasks, onMove, onDelete }: TaskColumnProps) {
  const statusDots: Record<string, string> = {
    todo: "bg-[#d4d4d2]",
    doing: "bg-amber-400",
    done: "bg-green-400",
  };

  return (
    <div className="flex flex-col min-w-[260px] flex-1" style={{ fontFamily: "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" }}>
      {/* Column Header */}
      <div className="flex items-center gap-2 px-1 py-2 mb-2">
        <div className={`w-2 h-2 rounded-full ${statusDots[status]}`} />
        <h3 className="text-sm font-semibold text-[#1d1d1f]">{title}</h3>
        <span className="text-xs text-[#9b9b9b] ml-auto">{tasks.length}</span>
      </div>

      {/* Task List */}
      <div className="flex-1 space-y-2 min-h-[150px]">
        {tasks.length === 0 ? (
          <div className="flex items-center justify-center py-10 text-[#d4d4d2]">
            <p className="text-xs">暂无任务</p>
          </div>
        ) : (
          tasks.map((task) => (
            <TaskCard key={task.id} task={task} onMove={onMove} onDelete={onDelete} />
          ))
        )}
      </div>
    </div>
  );
}
