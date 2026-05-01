import { apiRequest } from '../../core/api.js';
import { sanitizeHTML } from '../../shared/utils.js';

export async function getServiciosAsignados() {
  return await apiRequest('/reciclador/servicios');
}

export async function aceptarServicio(id) {
  return await apiRequest(`/reciclador/servicios/${id}/aceptar`, { method: 'PATCH' });
}

export async function rechazarServicio(id) {
  return await apiRequest(`/reciclador/servicios/${id}/rechazar`, { method: 'PATCH' });
}

export async function completarServicio(id, files) {
  const formData = new FormData();
  for (let i = 0; i < files.length; i++) {
    formData.append('fotos', files[i]);
  }
  return await apiRequest(`/reciclador/servicios/${id}/completar`, {
    method: 'POST',
    body: formData
  });
}