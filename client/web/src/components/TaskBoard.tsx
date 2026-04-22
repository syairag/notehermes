"use client";

import { useState, useEffect, useCallback } from "react";
import type { Task } from "@/types/task";
import { fetchTasks, updateTaskStatus, createTask, deleteTask } from "@/lib/api";
import TaskColumn from "./TaskColumn";

const columns = [
  { title: "待办", status: "todo" as const },
  { title: "进行中", status: "doing" as const },
  { title: "已完成", status: "done" as const },
];

export default function TaskBoard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [newPriority, setNewPriority] = useState<Task["priority"]>("medium");

  const loadTasks = useCallback(async () => {
    try {
      const data = await fetchTasks();
      setTasks(data);
    } catch { setError("加载失败"); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { loadTasks(); }, [loadTasks]);

  const handleMove = async (id: string, status: Task["status"]) => {
    try {
      const updated = await updateTaskStatus(id, status);
      setTasks((prev) => prev.map((t) => (t.id === updated.id ? updated : t)));
    } catch { setError("更新失败"); }
  };

  const handleDelete = async (id: string) => {
    try { await deleteTask(id); setTasks((prev) => prev.filter((t) => t.id !== id)); }
    catch { setError("删除失败"); }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    try {
      const created = await createTask({ title: newTitle.trim(), description: newDescription.trim() || undefined, priority: newPriority });
      setTasks((prev) => [...prev, created]);
      setNewTitle(""); setNewDescription(""); setNewPriority("medium"); setShowForm(false);
    } catch { setError("创建失败"); }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-6 h-6 border-2 border-[#e9e9e7] border-t-[#1d1d1f] rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div style={{ fontFamily: "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" }}>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <span className="text-3xl">☑️</span>
          <div>
            <h1 className="text-[30px] font-semibold text-[#1d1d1f] leading-tight">任务</h1>
            <p className="text-sm text-[#9b9b9b] mt-0.5">管理和跟踪您的任务</p>
          </div>
        </div>
        <button onClick={() => setShowForm(!showForm)} className="flex items-center gap-1.5 bg-[#1d1d1f] hover:bg-[#2d2d2f] text-white px-3.5 py-2 rounded-md text-sm font-medium transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
          </svg>
          新建任务
        </button>
      </div>

      {/* Error */}
      {error && <div className="mb-4 bg-[#fef3f2] border border-[#fecdca] text-[#c22] px-4 py-3 rounded-lg text-sm">{error}</div>}

      {/* Add Task Form - Notion style */}
      {showForm && (
        <form onSubmit={handleCreate} className="mb-6 bg-[#f7f7f5] border border-[#e9e9e7] rounded-lg p-4">
          <div className="flex flex-col sm:flex-row gap-3">
            <input type="text" value={newTitle} onChange={(e) => setNewTitle(e.target.value)} placeholder="任务标题" className="flex-1 px-0 py-2 border-0 bg-transparent text-sm text-[#1d1d1f] focus:outline-none placeholder:text-[#d4d4d2]" autoFocus required />
            <input type="text" value={newDescription} onChange={(e) => setNewDescription(e.target.value)} placeholder="描述（可选）" className="flex-1 px-0 py-2 border-0 bg-transparent text-sm text-[#1d1d1f] focus:outline-none placeholder:text-[#d4d4d2]" />
            <select value={newPriority} onChange={(e) => setNewPriority(e.target.value as Task["priority"])} className="px-3 py-1.5 border border-[#e9e9e7] rounded-md text-sm bg-white text-[#5e5e5e] focus:outline-none">
              <option value="low">低优先级</option>
              <option value="medium">中优先级</option>
              <option value="high">高优先级</option>
            </select>
            <button type="submit" className="bg-[#1d1d1f] hover:bg-[#2d2d2f] text-white px-4 py-1.5 rounded-md text-sm font-medium transition-colors">创建</button>
          </div>
        </form>
      )}

      {/* Kanban Board */}
      <div className="flex flex-col md:flex-row gap-4">
        {columns.map((col) => (
          <TaskColumn key={col.status} title={col.title} status={col.status} tasks={tasks.filter((t) => t.status === col.status)} onMove={handleMove} onDelete={handleDelete} />
        ))}
      </div>
    </div>
  );
}
