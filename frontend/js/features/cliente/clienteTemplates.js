export function dashboardClienteHTML() {
  return `
    <div class="page-wrapper">
      <div class="grid-3 mb-4">
        <div class="stat-card">
          <div class="stat-value">+</div>
          <div class="stat-label">Nueva Solicitud</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" id="totalServicios">0</div>
          <div class="stat-label">Servicios Totales</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" id="completados">0</div>
          <div class="stat-label">Completados</div>
        </div>
      </div>
      <div class="card">
        <div class="dashboard-tabs" style="padding: 0 1.5rem;">
          <button class="tab-btn active" data-tab="solicitar">Solicitar</button>
          <button class="tab-btn" data-tab="servicios">Mis Servicios</button>
        </div>
        <div class="card-body" id="tabContent"></div>
      </div>
    </div>`;
}

export function formSolicitarHTML() {
  return `
    <div>
      <div class="card" style="max-width: 600px; margin: 0 auto;">
        <div class="card-header">Nueva Solicitud de Recolección</div>
        <div class="card-body">
          <form id="formSolicitar">
            <div class="form-group">
              <label class="form-label" for="descripcion">Descripción de los residuos</label>
              <textarea class="form-control" id="descripcion" placeholder="Ej: Cartón, plástico, 2 bolsas grandes..." required></textarea>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Enviar Solicitud</button>
          </form>
          <div id="solicitudMsg" class="mt-4"></div>
        </div>
      </div>
    </div>`;
}

export function serviciosTableHTML(servicios) {
  if (!servicios.length) {
    return `<div class="text-center" style="padding: 3rem; color: var(--text-secondary);">
      <p style="font-size: 1.25rem;">📋 No tienes servicios aún</p>
      <p>Solicita tu primer servicio de recolección.</p>
    </div>`;
  }
  let rows = '';
  servicios.forEach(s => {
    rows += `
      <tr>
        <td><strong>#${s.id}</strong></td>
        <td>${s.descripcion}</td>
        <td><span class="status-badge status-${s.estado}">${s.estado}</span></td>
        <td>${new Date(s.fecha_solicitud).toLocaleDateString()}</td>
        <td>
          ${s.estado === 'completado' ? 
            `<button class="btn btn-warning btn-sm" data-calificar="${s.id}">⭐ Calificar</button>` : 
            `<span style="color: var(--text-secondary);">—</span>`}
        </td>
      </tr>`;
  });
  return `<div class="table-responsive"><table class="table">
    <thead><tr><th>ID</th><th>Descripción</th><th>Estado</th><th>Fecha</th><th>Acción</th></tr></thead>
    <tbody>${rows}</tbody></table></div>`;
}