import io
from datetime import datetime
from app.infrastructure.repositories.service_repo import ServiceRepository
from app.infrastructure.models import Service

def test_completar_servicio_con_fotos(client, reciclador_token, reciclador_user, db_session):
    # Preparar servicio en estado aceptado para el reciclador
    repo = ServiceRepository(db_session)
    service = Service(
        cliente_id=999,
        reciclador_id=reciclador_user.id,
        descripcion="Fotos test",
        estado="aceptado",
        fecha_solicitud=datetime.utcnow()
    )
    repo.create(service)
    # Crear archivo de imagen falso
    fake_img = io.BytesIO(b"fake image content")
    fake_img.name = "test.jpg"
    response = client.post(
        f"/api/v1/reciclador/servicios/{service.id}/completar",
        files={"fotos": ("test.jpg", fake_img, "image/jpeg")},
        headers={"Authorization": f"Bearer {reciclador_token}"}
    )
    assert response.status_code == 200
    assert response.json()["mensaje"] == "Servicio completado"