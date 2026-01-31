import axios from 'axios';

const API = axios.create({
  baseURL: '/api',
});

// Add token to every request
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  signup: (username, password) => API.post('/auth/signup', { username, password }),
  login: (username, password) => API.post('/auth/login', { username, password }),
};

export const notesAPI = {
  getNotes: () => API.get('/notes'),
  createNote: (content, masterKey) => API.post('/notes', { content, master_key: masterKey }),
  decryptNote: (noteId, masterKey) => API.post(`/notes/${noteId}/decrypt`, { master_key: masterKey }),
  updateNote: (noteId, content, masterKey) => API.put(`/notes/${noteId}`, { content, master_key: masterKey }),
  deleteNote: (noteId) => API.delete(`/notes/${noteId}`),
};

export default API;
