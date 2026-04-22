import axios from "axios";
import type { Task } from "@/types/task";

// 动态获取后端地址：
// - 浏览器端：使用当前页面的主机名，端口改为 8000
// - SSR 端：使用环境变量或默认 localhost
function getBaseUrl(): string {
  if (typeof window !== "undefined") {
    return `${window.location.protocol}//${window.location.hostname}:8000`;
  }
  return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
}

const api = axios.create({
  baseURL: getBaseUrl(),
  timeout: 15000,
});

// Map backend snake_case response to frontend camelCase Task type
function mapTask(raw: Record<string, unknown>): Task {
  return {
    id: String(raw.id),
    title: raw.title as string,
    description: (raw.description as string) || "",
    status: (raw.status as Task["status"]) || "todo",
    priority: (raw.priority as Task["priority"]) || "medium",
    createdAt: String(raw.created_at),
    updatedAt: String(raw.updated_at),
  };
}

export async function fetchTasks(): Promise<Task[]> {
  const res = await api.get<Record<string, unknown>>("/api/v1/tasks");
  return res.data.map(mapTask);
}

export async function createTask(data: {
  title: string;
  description?: string;
  priority?: "low" | "medium" | "high";
}): Promise<Task> {
  const res = await api.post<Record<string, unknown>>("/api/v1/tasks", data);
  return mapTask(res.data);
}

export async function updateTaskStatus(
  id: string,
  status: Task["status"]
): Promise<Task> {
  const res = await api.put<Record<string, unknown>>(
    `/api/v1/tasks/${id}/status`,
    { status }
  );
  return mapTask(res.data);
}

export async function deleteTask(id: string): Promise<void> {
  await api.delete(`/api/v1/tasks/${id}`);
}

// --- Email types ---

export interface Email {
  id: string;
  subject: string;
  sender: string;
  date: string;
  hasAISummary: boolean;
  summary: string;
}

export async function getEmails(): Promise<Email[]> {
  const res = await api.get<Record<string, unknown>>("/api/v1/emails/");
  return res.data.map((raw: Record<string, unknown>) => ({
    id: String(raw.id),
    subject: (raw.subject as string) || "",
    sender: (raw.sender as string) || "",
    date: String(raw.date || raw.created_at || ""),
    hasAISummary: Boolean(raw.has_ai_summary || raw.summary),
    summary: (raw.summary as string) || "",
  }));
}

export async function syncEmails(): Promise<{ synced: number; message?: string; emails?: unknown[] }> {
  const res = await api.post<Record<string, unknown>>("/api/v1/emails/sync");
  return { synced: Number(res.data.synced ?? 0), message: res.data.message as string, emails: res.data.emails as unknown[] };
}

export async function configureExchange(data: {
  server?: string;
  email: string;
  password: string;
  auth_type?: string;
  limit?: number;
}): Promise<{ status: string; email: string }> {
  const res = await api.post<Record<string, unknown>>("/api/v1/emails/configure/exchange", data);
  return { status: res.data.status as string, email: res.data.email as string };
}

// --- Note types ---

export interface Note {
  id: string;
  title: string;
  content: string;
  tags: string[];
  date: string;
}

export async function getNotes(): Promise<Note[]> {
  const res = await api.get<Record<string, unknown>>("/api/v1/notes/");
  return res.data.map((raw: Record<string, unknown>) => ({
    id: String(raw.id),
    title: (raw.title as string) || "",
    content: (raw.content as string) || "",
    tags: (raw.tags as string[]) || [],
    date: String(raw.date || raw.created_at || ""),
  }));
}

export async function createNote(data: {
  title: string;
  content: string;
  tags?: string[];
}): Promise<Note> {
  const res = await api.post<Record<string, unknown>>("/api/v1/notes/", data);
  return {
    id: String(res.data.id),
    title: (res.data.title as string) || "",
    content: (res.data.content as string) || "",
    tags: (res.data.tags as string[]) || [],
    date: String(res.data.date || res.data.created_at || ""),
  };
}

export async function deleteNote(id: string): Promise<void> {
  await api.delete(`/api/v1/notes/${id}`);
}
