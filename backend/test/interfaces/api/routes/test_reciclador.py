from datetime import datetime
from app.infrastructure.repositories.service_repo import ServiceRepository
from app.infrastructure.models import Service

def test_reciclador_get_services_requires_auth(client):
    response = client.get("/api/v1/reciclador/servicios")
    assert response.status_code == 401

def test_reciclador_accept_service(client, reciclador_token, reciclador_user, db_session):
    # Crear un servicio asignado al reciclador que acaba de crear el fixture
    repo = ServiceRepository(db_session)
    service = Service(
        cliente_id=999,  # cliente ficticio
        reciclador_id=reciclador_user.id,
        descripcion="Test",
        estado="asignado",
        fecha_solicitud=datetime.utcnow()
    )
    repo.create(service)
    # Llamar con el token del reciclador
    response = client.patch(
        f"/api/v1/reciclador/servicios/{service.id}/aceptar",
        headers={"Authorization": f"Bearer {reciclador_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "aceptado"