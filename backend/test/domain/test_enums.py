from app.domain.enums import UserRole, ServiceStatus

def test_user_role_values():
    assert UserRole.CLIENTE == "cliente"
    assert UserRole.RECICLADOR == "reciclador"
    assert UserRole.SUPERADMIN == "superadmin"

def test_service_status_values():
    assert ServiceStatus.PENDIENTE == "pendiente"
    assert ServiceStatus.COMPLETADO == "completado"