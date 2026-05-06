from app.domain.entities import Usuario, Servicio
from app.domain.enums import UserRole, ServiceStatus

def test_usuario_creation():
    user = Usuario(
        email="test@test.com",
        nombre="Test",
        rol=UserRole.CLIENTE
    )
    assert user.rol == UserRole.CLIENTE

def test_servicio_default_state():
    service = Servicio(
        cliente_id=1,
        descripcion="Reciclaje"
    )
    assert service.estado == ServiceStatus.PENDIENTE