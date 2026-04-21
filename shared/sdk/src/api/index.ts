import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NOTEHERMES_API_URL || 'http://localhost:8000/api/v1',
});

export const emailApi = {
  list: () => api.get('/emails/'),
  get: (id: string) => api.get(`/emails/${id}`),
  summarize: (id: string) => api.post(`/emails/summarize/${id}`),
};

export const noteApi = {
  list: () => api.get('/notes/'),
  create: (data: any) => api.post('/notes/', data),
};

export const taskApi = {
  list: () => api.get('/tasks/'),
  create: (data: any) => api.post('/tasks/', data),
};

export default api;
