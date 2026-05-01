import { apiRequest } from '../../core/api.js';
import { sanitizeHTML } from '../../shared/utils.js';

export async function listarUsuarios(rolFilter = '') {
  const query = rolFilter ? `?rol=${rolFilter}` : '';
  return await apiRequest(`/admin/usuarios${query}`);
}

export async function listarServicios() {
  return await apiRequest('/admin/servicios');
}

export async function listarPendientes() {
  return await apiRequest('/admin/servicios/pendientes');
}

export async function asignarReciclador(servicioId, recicladorId) {
  return await apiRequest(`/admin/servicios/${servicioId}/asignar`, {
    method: 'PATCH',
    body: JSON.stringify({ reciclador_id: recicladorId })
  });
}

export async function listarCalificaciones() {
  return await apiRequest('/admin/calificaciones');
}