import { getUserRole } from './auth.js';

export function requireRole(role) {
  const userRole = getUserRole();
  if (userRole !== role) {
    window.location.hash = '#/login';
    return false;
  }
  return true;
}