import { apiRequest } from '../../core/api.js';
import { setToken, getUserRole } from '../../core/auth.js';

export async function register(userData) {
  const data = await apiRequest('/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData)
  });
  setToken(data.access_token);
  return getUserRole();
}