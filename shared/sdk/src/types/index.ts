export interface User {
  id: string;
  email: string;
  name: string;
}

export interface Email {
  id: string;
  subject: string;
  from: string;
  body: string;
  summary?: string;
}

export interface Note {
  id: string;
  title: string;
  content: string;
  tags: string[];
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'todo' | 'doing' | 'done';
  priority: 'low' | 'medium' | 'high' | 'urgent';
}
