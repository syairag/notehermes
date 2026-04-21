"use client";

import type { Task } from "@/types/task";
import TaskCard from "./TaskCard";

interface TaskColumnProps {
  title: string;
  icon: string;
  status: Task["status"];
  tasks: Task[];
  accentColor: string;
  onMove: (id: string, status: Task["status"]) => void;
  onDelete: (id: string) => void;
}

export default function TaskColumn({
  title,
  icon,
  status,
  tasks,
  accentColor,
  onMove,
  onDelete,
}: TaskColumnProps) {
  return (
    <div className="flex flex-col min-w-[280px] flex-1">
      {/* Column Header */}
      <div className={`flex items-center gap-2 px-4 py-3 rounded-t-xl ${accentColor}`}>
        <span className="text-lg">{icon}</span>
        <h3 className="font-bold text-white text-sm uppercase tracking-wide">
          {title}
        </h3>
        <span className="ml-auto bg-white/20 text-white text-xs font-semibold px-2 py-0.5 rounded-full">
          {tasks.length}
        </span>
      </div>

      {/* Task List */}
      <div className="flex-1 bg-gray-100/80 rounded-b-xl p-3 space-y-3 min-h-[200px]">
        {tasks.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-10 text-gray-400">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-10 w-10 mb-2 opacity-50"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={1}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
              />
            </svg>
            <p className="text-xs font-medium">No tasks</p>
          </div>
        ) : (
          tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onMove={onMove}
              onDelete={onDelete}
            />
          ))
        )}
      </div>
    </div>
  );
}
