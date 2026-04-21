"use client";

import type { Task } from "@/types/task";

const priorityColors: Record<Task["priority"], string> = {
  high: "border-l-red-500",
  medium: "border-l-yellow-500",
  low: "border-l-green-500",
};

const priorityBadgeColors: Record<Task["priority"], string> = {
  high: "bg-red-100 text-red-700",
  medium: "bg-yellow-100 text-yellow-700",
  low: "bg-green-100 text-green-700",
};

interface TaskCardProps {
  task: Task;
  onMove: (id: string, status: Task["status"]) => void;
  onDelete: (id: string) => void;
}

export default function TaskCard({ task, onMove, onDelete }: TaskCardProps) {
  return (
    <div
      className={`bg-white rounded-lg shadow-sm border border-gray-200 border-l-4 ${priorityColors[task.priority]} p-4 hover:shadow-md transition-shadow`}
    >
      <div className="flex items-start justify-between gap-2">
        <h4 className="font-semibold text-gray-900 text-sm leading-tight flex-1">
          {task.title}
        </h4>
        <button
          onClick={() => onDelete(task.id)}
          className="text-gray-400 hover:text-red-500 transition-colors shrink-0"
          aria-label="Delete task"
          title="Delete task"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      {task.description && (
        <p className="text-gray-500 text-xs mt-1.5 line-clamp-2">
          {task.description}
        </p>
      )}

      <div className="flex items-center justify-between mt-3">
        <span
          className={`text-[10px] font-medium px-2 py-0.5 rounded-full uppercase tracking-wide ${priorityBadgeColors[task.priority]}`}
        >
          {task.priority}
        </span>

        <div className="flex gap-1">
          {task.status !== "todo" && (
            <button
              onClick={() =>
                onMove(task.id, task.status === "done" ? "doing" : "todo")
              }
              className="text-gray-400 hover:text-blue-600 transition-colors p-1 rounded hover:bg-gray-100"
              title={task.status === "done" ? "Move to Doing" : "Move to To Do"}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-3.5 w-3.5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M15 19l-7-7 7-7"
                />
              </svg>
            </button>
          )}
          {task.status !== "done" && (
            <button
              onClick={() =>
                onMove(task.id, task.status === "todo" ? "doing" : "done")
              }
              className="text-gray-400 hover:text-blue-600 transition-colors p-1 rounded hover:bg-gray-100"
              title={task.status === "todo" ? "Move to Doing" : "Move to Done"}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-3.5 w-3.5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
