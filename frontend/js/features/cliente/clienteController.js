import { apiRequest } from '../../core/api.js';
import { getUserId } from '../../core/auth.js';
import { sanitizeHTML } from '../../shared/utils.js';

export async function solicitarServicio(descripcion) {
  return await apiRequest('/servicios', {
    method: 'POST',
    body: JSON.stringify({ descripcion: sanitizeHTML(descripcion) })
  });
}

export async function getMisServicios() {
  return await apiRequest('/servicios');
}

export async function getServicioDetalle(id) {
  return await apiRequest(`/servicios/${id}`);
}

export async function calificarServicio(servicioId, puntuacion, comentario) {
  return await apiRequest(`/servicios/${servicioId}/calificar`, {
    method: 'POST',
    body: JSON.stringify({
      puntuacion: parseInt(puntuacion),
      comentario: sanitizeHTML(comentario)
    })
  });
}