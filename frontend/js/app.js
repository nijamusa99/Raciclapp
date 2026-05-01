import { getToken, getUserRole, clearToken, getUserId } from './core/auth.js';
import { login } from './features/auth/login.js';
import { register } from './features/auth/register.js';
import {
  solicitarServicio, getMisServicios, getServicioDetalle, calificarServicio
} from './features/cliente/clienteController.js';
import {
  dashboardClienteHTML, formSolicitarHTML, serviciosTableHTML
} from './features/cliente/clienteTemplates.js';
import {
  getServiciosAsignados, aceptarServicio, rechazarServicio, completarServicio
} from './features/reciclador/recicladorController.js';
import {
  recicladorDashboardHTML, formCompletarHTML
} from './features/reciclador/recicladorTemplates.js';
import {
  listarUsuarios, listarServicios, listarPendientes, asignarReciclador, listarCalificaciones
} from './features/admin/adminController.js';
import {
  adminDashboardHTML, usuariosTableHTML, serviciosAdminHTML, calificacionesHTML
} from './features/admin/adminTemplates.js';
import { sanitizeHTML } from './shared/utils.js';

const app = document.getElementById('app');

// ---------- NAVBAR ----------
function renderNavbar(role) {
  const roleLabels = { cliente: 'Cliente', reciclador: 'Reciclador', superadmin: 'Admin' };
  return `
    <nav class="navbar">
      <a href="#/" class="navbar-brand">♻️ Reciclap</a>
      <div class="navbar-user">
        <span class="navbar-role">${roleLabels[role] || role}</span>
        <button id="logoutBtn" class="btn btn-outline btn-sm">Cerrar sesión</button>
      </div>
    </nav>`;
}

// ---------- ROUTER ----------
async function router() {
  const path = window.location.hash.slice(1) || '/';
  const role = getUserRole();

  // Si no hay token y no es registro, mostrar login
  if (!getToken() && path !== '/register') {
    renderLogin();
    return;
  }

  // Si no hay token pero estamos en registro, mostrar registro
  if (!getToken() && path === '/register') {
    renderRegister();
    return;
  }

  // Si hay token pero no hay rol (raro), mostrar login
  if (!role) {
    renderLogin();
    return;
  }

  // Rutas por rol
  switch (role) {
    case 'cliente':
      renderClientePage();
      break;
    case 'reciclador':
      renderRecicladorPage();
      break;
    case 'superadmin':
      renderAdminPage();
      break;
    default:
      renderLogin();
  }
}

// ---------- LOGIN ----------
function renderLogin() {
  app.innerHTML = `
    <div class="container" style="margin-top: 5rem;">
      <div class="card" style="max-width:400px; margin:0 auto;">
        <h2 class="text-center">Iniciar Sesión</h2>
        <form id="loginForm">
          <div class="form-group"><input class="form-control" id="email" placeholder="Email" required></div>
          <div class="form-group"><input class="form-control" id="password" type="password" placeholder="Contraseña" required></div>
          <button type="submit" class="btn btn-primary" style="width:100%">Entrar</button>
        </form>
        <p class="text-center mt-2"><a href="#/register">Registrarse</a></p>
        <div id="loginError"></div>
      </div>
    </div>`;

  document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    try {
      const role = await login(email, password);
      window.location.hash = '#/dashboard';
    } catch (err) {
      document.getElementById('loginError').innerHTML = `<div class="alert alert-danger">${sanitizeHTML(err.message)}</div>`;
    }
  });
}

// ---------- REGISTER ----------
function renderRegister() {
  app.innerHTML = `
    <div class="container" style="margin-top: 3rem;">
      <div class="card" style="max-width:600px; margin:0 auto;">
        <h2 class="text-center">Registro</h2>
        <form id="regForm">
          <div class="form-group"><input class="form-control" id="regEmail" placeholder="Email" required></div>
          <div class="form-group"><input class="form-control" id="regPassword" type="password" placeholder="Contraseña" required></div>
          <div class="form-group"><input class="form-control" id="regNombre" placeholder="Nombre completo" required></div>
          <div class="form-group"><input class="form-control" id="regTelefono" placeholder="Teléfono"></div>
          <div class="form-group">
            <select class="form-control" id="regRol" required>
              <option value="cliente">Cliente (Edificio)</option>
              <option value="reciclador">Reciclador</option>
            </select>
          </div>
          <div id="extraFields"></div>
          <button type="submit" class="btn btn-primary" style="width:100%">Registrarse</button>
        </form>
        <p class="text-center mt-2"><a href="#/login">Iniciar Sesión</a></p>
        <div id="regError"></div>
      </div>
    </div>`;

  const rolSelect = document.getElementById('regRol');
  const extraFields = document.getElementById('extraFields');

  function updateExtraFields() {
    if (rolSelect.value === 'cliente') {
      extraFields.innerHTML = `
        <div class="form-group"><input class="form-control" id="regEdificio" placeholder="Nombre del edificio"></div>
        <div class="form-group"><input class="form-control" id="regDireccion" placeholder="Dirección"></div>
        <div class="form-group"><input class="form-control" id="regCiudad" placeholder="Ciudad"></div>`;
    } else {
      extraFields.innerHTML = `
        <div class="form-group"><input class="form-control" id="regVehiculo" placeholder="Tipo de vehículo"></div>`;
    }
  }

  rolSelect.addEventListener('change', updateExtraFields);
  updateExtraFields();

  document.getElementById('regForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const rol = rolSelect.value;
    const body = {
      email: document.getElementById('regEmail').value,
      password: document.getElementById('regPassword').value,
      nombre: document.getElementById('regNombre').value,
      telefono: document.getElementById('regTelefono').value,
      rol
    };
    if (rol === 'cliente') {
      body.nombre_edificio = document.getElementById('regEdificio').value;
      body.direccion = document.getElementById('regDireccion').value;
      body.ciudad = document.getElementById('regCiudad').value;
    } else {
      body.tipo_vehiculo = document.getElementById('regVehiculo').value;
    }
    try {
      const role = await register(body);
      window.location.hash = '#/dashboard';
    } catch (err) {
      document.getElementById('regError').innerHTML = `<div class="alert alert-danger">${sanitizeHTML(err.message)}</div>`;
    }
  });
}

// ---------- CLIENTE ----------
function renderClientePage() {
  app.innerHTML = `
    ${renderNavbar('cliente')}
    <div class="container">
      ${dashboardClienteHTML()}
    </div>`;

  document.getElementById('logoutBtn').addEventListener('click', () => {
    clearToken();
    window.location.hash = '#/login';
  });

  // Tabs
  const tabButtons = document.querySelectorAll('.tab-btn');
  tabButtons.forEach(btn => btn.addEventListener('click', (e) => {
    tabButtons.forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    const tab = e.target.dataset.tab;
    if (tab === 'solicitar') mostrarSolicitar();
    else if (tab === 'servicios') mostrarServicios();
  }));

  mostrarSolicitar();
}

async function mostrarSolicitar() {
  const tabContent = document.getElementById('tabContent');
  tabContent.innerHTML = formSolicitarHTML();

  document.getElementById('formSolicitar').addEventListener('submit', async (e) => {
    e.preventDefault();
    const descripcion = document.getElementById('descripcion').value;
    try {
      const servicio = await solicitarServicio(descripcion);
      document.getElementById('solicitudMsg').innerHTML = `<div class="alert alert-success">Solicitud #${servicio.id} creada correctamente.</div>`;
      document.getElementById('descripcion').value = '';
    } catch (err) {
      document.getElementById('solicitudMsg').innerHTML = `<div class="alert alert-danger">${sanitizeHTML(err.message)}</div>`;
    }
  });
}

async function mostrarServicios() {
  const tabContent = document.getElementById('tabContent');
  tabContent.innerHTML = '<div class="card"><p class="text-center mt-4">Cargando...</p></div>';
  try {
    const servicios = await getMisServicios();
    tabContent.innerHTML = serviciosTableHTML(servicios);
    // Eventos para calificar
    document.querySelectorAll('[data-calificar]').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = btn.dataset.calificar;
        const puntuacion = prompt('Puntuación (1-5):');
        if (!puntuacion || isNaN(puntuacion) || puntuacion < 1 || puntuacion > 5) return;
        const comentario = prompt('Comentario (opcional):') || '';
        try {
          await calificarServicio(id, puntuacion, comentario);
          alert('Calificación registrada');
          mostrarServicios();
        } catch (err) {
          alert('Error: ' + err.message);
        }
      });
    });
  } catch (err) {
    tabContent.innerHTML = `<div class="alert alert-danger">${sanitizeHTML(err.message)}</div>`;
  }
}

// ---------- RECICLADOR ----------
function renderRecicladorPage() {
  app.innerHTML = `
    ${renderNavbar('reciclador')}
    <div class="container" id="recicladorContent"></div>`;

  document.getElementById('logoutBtn').addEventListener('click', () => {
    clearToken();
    window.location.hash = '#/login';
  });

  cargarReciclador();
}

async function cargarReciclador() {
  const content = document.getElementById('recicladorContent');
  content.innerHTML = '<div class="card"><p class="text-center mt-4">Cargando...</p></div>';
  try {
    const servicios = await getServiciosAsignados();
    content.innerHTML = recicladorDashboardHTML(servicios);

    // Eventos aceptar/rechazar
    document.querySelectorAll('[data-accion="aceptar"]').forEach(btn => {
      btn.addEventListener('click', async () => {
        await aceptarServicio(btn.dataset.id);
        cargarReciclador();
      });
    });
    document.querySelectorAll('[data-accion="rechazar"]').forEach(btn => {
      btn.addEventListener('click', async () => {
        await rechazarServicio(btn.dataset.id);
        cargarReciclador();
      });
    });
    document.querySelectorAll('[data-accion="completar"]').forEach(btn => {
      btn.addEventListener('click', () => {
        const formHtml = formCompletarHTML(btn.dataset.id);
        content.insertAdjacentHTML('beforeend', formHtml);
        initFormCompletar(btn.dataset.id);
      });
    });
  } catch (err) {
    content.innerHTML = `<div class="alert alert-danger">${sanitizeHTML(err.message)}</div>`;
  }
}

function initFormCompletar(servicioId) {
  const dropArea = document.getElementById('dropArea');
  const input = document.getElementById('fotosInput');
  dropArea.addEventListener('click', () => input.click());
  dropArea.addEventListener('dragover', e => e.preventDefault());
  dropArea.addEventListener('drop', e => {
    e.preventDefault();
    input.files = e.dataTransfer.files;
    mostrarPreview(input.files);
  });
  input.addEventListener('change', () => mostrarPreview(input.files));

  document.getElementById('btnCompletar').addEventListener('click', async () => {
    const files = input.files;
    if (!files.length) return alert('Selecciona al menos una foto');
    try {
      await completarServicio(servicioId, files);
      document.getElementById('formCompletar').remove();
      alert('Servicio completado exitosamente');
      cargarReciclador();
    } catch (err) {
      alert('Error: ' + err.message);
    }
  });
}

function mostrarPreview(files) {
  const preview = document.getElementById('previewFotos');
  preview.innerHTML = '';
  for (let i = 0; i < files.length; i++) {
    const reader = new FileReader();
    reader.onload = e => {
      const img = document.createElement('img');
      img.src = e.target.result;
      preview.appendChild(img);
    };
    reader.readAsDataURL(files[i]);
  }
}

// ---------- ADMIN ----------
function renderAdminPage() {
  app.innerHTML = `
    ${renderNavbar('superadmin')}
    <div class="container">${adminDashboardHTML()}</div>`;

  document.getElementById('logoutBtn').addEventListener('click', () => {
    clearToken();
    window.location.hash = '#/login';
  });

  const tabButtons = document.querySelectorAll('.tab-btn');
  tabButtons.forEach(btn => btn.addEventListener('click', (e) => {
    tabButtons.forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    const tab = e.target.dataset.tab;
    if (tab === 'usuarios') cargarUsuarios();
    else if (tab === 'servicios') cargarServiciosAdmin();
    else if (tab === 'calificaciones') cargarCalificaciones();
  }));

  cargarUsuarios();
}

async function cargarUsuarios() {
  const tabContent = document.getElementById('tabContent');
  tabContent.innerHTML = '<p>Cargando...</p>';
  try {
    const usuarios = await listarUsuarios();
    tabContent.innerHTML = usuariosTableHTML(usuarios);
  } catch (err) {
    tabContent.innerHTML = `<div class="alert alert-danger">${sanitizeHTML(err.message)}</div>`;
  }
}

async function cargarServiciosAdmin() {
  const tabContent = document.getElementById('tabContent');
  tabContent.innerHTML = '<p>Cargando...</p>';
  try {
    const servicios = await listarServicios();
    tabContent.innerHTML = serviciosAdminHTML(servicios);
    agregarEventosAsignar();
  } catch (err) {
    tabContent.innerHTML = `<div class="alert alert-danger">${sanitizeHTML(err.message)}</div>`;
  }
}

async function cargarPendientes() {
  try {
    const servicios = await listarPendientes();
    document.getElementById('tabContent').innerHTML = serviciosAdminHTML(servicios, true);
    agregarEventosAsignar();
  } catch (err) {
    alert(err.message);
  }
}

function agregarEventosAsignar() {
  document.querySelectorAll('[data-asignar]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const servicioId = btn.dataset.asignar;
      const input = document.getElementById(`recId-${servicioId}`);
      const recicladorId = input ? input.value : null;
      if (!recicladorId) return alert('Ingresa el ID del reciclador');
      try {
        await asignarReciclador(servicioId, parseInt(recicladorId));
        alert('Asignado correctamente');
        cargarServiciosAdmin();
      } catch (err) {
        alert('Error: ' + err.message);
      }
    });
  });
}

async function cargarCalificaciones() {
  const tabContent = document.getElementById('tabContent');
  tabContent.innerHTML = '<p>Cargando...</p>';
  try {
    const calificaciones = await listarCalificaciones();
    tabContent.innerHTML = calificacionesHTML(calificaciones);
  } catch (err) {
    tabContent.innerHTML = `<div class="alert alert-danger">${sanitizeHTML(err.message)}</div>`;
  }
}

// ---------- INICIO ----------
window.addEventListener('hashchange', router);
router();