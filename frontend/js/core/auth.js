// Servicio de autenticación con token en memoria
let memoryToken = null;

export function getToken() {
  return memoryToken;
}

export function setToken(token) {
  memoryToken = token;
}

export function clearToken() {
  memoryToken = null;
}

export function decodeToken() {
  const token = getToken();
  if (!token) return null;
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch {
    return null;
  }
}

export function getUserRole() {
  const decoded = decodeToken();
  return decoded ? decoded.rol : null;
}

export function getUserId() {
  const decoded = decodeToken();
  return decoded ? parseInt(decoded.sub) : null;
}