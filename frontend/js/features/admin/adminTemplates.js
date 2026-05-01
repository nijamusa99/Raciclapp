export function adminDashboardHTML() {
  return `
    <div class="page-wrapper">
      <div class="card">
        <div class="dashboard-tabs" style="padding: 0 1.5rem;">
          <button class="tab-btn active" data-tab="usuarios">👥 Usuarios</button>
          <button class="tab-btn" data-tab="servicios">📋 Servicios</button>
          <button class="tab-btn" data-tab="calificaciones">⭐ Calificaciones</button>
        </div>
        <div class="card-body" id="tabContent"></div>
      </div>
    </div>`;
}

export function usuariosTableHTML(usuarios) {
  let rows = '';
  usuarios.forEach(u => {
    rows += `<tr>
      <td><strong>#${u.id}</strong></td>
      <td>${u.email}</td>
      <td>${u.nombre}</td>
      <td><span class="status-badge ${u.rol === 'superadmin' ? 'status-aceptado' : u.rol === 'reciclador' ? 'status-asignado' : 'status-pendiente'}">${u.rol}</span></td>
      <td>${u.activo ? '✅' : '❌'}</td>
    </tr>`;
  });
  return `<div class="table-responsive"><table class="table">
    <thead><tr><th>ID</th><th>Email</th><th>Nombre</th><th>Rol</th><th>Activo</th></tr></thead>
    <tbody>${rows}</tbody></table></div>`;
}

export function serviciosAdminHTML(servicios, esPendiente = false) {
  if (!servicios.length) {
    return `<div class="text-center" style="padding: 3rem; color: var(--text-secondary);">No hay servicios ${esPendiente ? 'pendientes' : 'registrados'}.</div>`;
  }
  let rows = '';
  servicios.forEach(s => {
    rows += `<tr>
      <td><strong>#${s.id}</strong></td>
      <td>${s.descripcion}</td>
      <td>#${s.cliente_id}</td>
      <td>${s.reciclador_id ? '#' + s.reciclador_id : '—'}</td>
      <td><span class="status-badge status-${s.estado}">${s.estado}</span></td>
      <td>${s.estado === 'pendiente' ? 
        `<div class="btn-group">
          <input type="number" class="form-control" placeholder="ID Reciclador" style="width: 130px;" id="recId-${s.id}">
          <button class="btn btn-primary btn-sm" data-asignar="${s.id}">Asignar</button>
        </div>` : '—'}
      </td></tr>`;
  });
  return `<div>
    ${esPendiente ? '<button class="btn btn-secondary btn-sm mb-4" onclick="cargarServiciosAdmin()">← Ver todos</button>' : '<button class="btn btn-warning btn-sm mb-4" onclick="cargarPendientes()">🔔 Ver pendientes</button>'}
    <div class="table-responsive"><table class="table">
      <thead><tr><th>ID</th><th>Descripción</th><th>Cliente</th><th>Reciclador</th><th>Estado</th><th>Acción</th></tr></thead>
      <tbody>${rows}</tbody></table></div></div>`;
}

export function calificacionesHTML(calificaciones) {
  if (!calificaciones.length) return '<div class="text-center" style="padding: 3rem; color: var(--text-secondary);">Aún no hay calificaciones registradas.</div>';
  let rows = '';
  calificaciones.forEach(c => {
    rows += `<tr>
      <td>#${c.servicio_id}</td>
      <td>#${c.calificador_id}</td>
      <td>#${c.calificado_id}</td>
      <td>${'⭐'.repeat(c.puntuacion)}</td>
      <td>${c.comentario || '—'}</td>
      <td>${new Date(c.fecha).toLocaleDateString()}</td>
    </tr>`;
  });
  return `<div class="table-responsive"><table class="table">
    <thead><tr><th>Servicio</th><th>Cliente</th><th>Reciclador</th><th>Puntuación</th><th>Comentario</th><th>Fecha</th></tr></thead>
    <tbody>${rows}</tbody></table></div>`;
}