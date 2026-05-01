import { apiRequest } from '../../core/api.js';
import { setToken, getUserRole } from '../../core/auth.js';

export async function login(email, password) {
  const data = await apiRequest('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  });
  setToken(data.access_token);
  return getUserRole();
}