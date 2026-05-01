// Adaptador HTTP centralizado
import { getToken } from './auth.js';

const API_BASE = 'http://localhost:8000/api/v1';

export async function apiRequest(path, options = {}) {
  const token = getToken();
  const headers = { 'X-CSRF-Token': generateCsrf() };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }

  const config = { ...options, headers: { ...headers, ...options.headers } };

  try {
    const response = await fetch(`${API_BASE}${path}`, config);
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.detail || `Error ${response.status}`);
    }

    return data;
  } catch (error) {
    throw error;
  }
}

function generateCsrf() {
  // Derivar de token o usar un valor aleatorio
  return Math.random().toString(36).slice(2);
}