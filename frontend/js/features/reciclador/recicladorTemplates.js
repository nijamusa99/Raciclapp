import { sanitizeHTML } from '../../shared/utils.js';

export function recicladorDashboardHTML(servicios) {
  let html = `
    <div class="card">
      <div class="card-header">Servicios Asignados</div>`;

  if (!servicios.length) {
    html += '<p class="text-center mt-4">No tienes servicios asignados.</p>';
    html += '</div>';
    return html;
  }

  html += `
      <div class="table-responsive">
        <table class="table">
          <thead><tr><th>ID</th><th>Descripción</th><th>Estado</th><th>Acción</th></tr></thead>
          <tbody>`;

  servicios.forEach(s => {
    html += `<tr>
      <td>#${s.id}</td>
      <td>${sanitizeHTML(s.descripcion)}</td>
      <td><span class="status-badge status-${s.estado}">${s.estado}</span></td>
      <td>
        <div class="btn-group">`;
    if (s.estado === 'asignado') {
      html += `<button class="btn btn-primary btn-sm" data-accion="aceptar" data-id="${s.id}">Aceptar</button>
               <button class="btn btn-danger btn-sm" data-accion="rechazar" data-id="${s.id}">Rechazar</button>`;
    } else if (s.estado === 'aceptado') {
      html += `<button class="btn btn-primary btn-sm" data-accion="completar" data-id="${s.id}">Completar</button>`;
    }
    html += `</div></td></tr>`;
  });

  html += '</tbody></table></div></div>';
  return html;
}

export function formCompletarHTML(servicioId) {
  return `
    <div class="card mt-4" id="formCompletar">
      <div class="card-header">Completar Servicio #${servicioId}</div>
      <div class="file-upload-area" id="dropArea">
        <p>Arrastra fotos aquí o haz clic para seleccionar</p>
        <input type="file" id="fotosInput" multiple accept="image/jpeg,image/png">
      </div>
      <div class="preview-grid" id="previewFotos"></div>
      <button class="btn btn-primary" id="btnCompletar">Confirmar Entrega</button>
    </div>`;
}