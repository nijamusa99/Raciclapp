from app.infrastructure.repositories.service_repo import ServiceRepository
from app.infrastructure.models import Service
from datetime import datetime

def test_create_and_list_services(db_session):
    repo = ServiceRepository(db_session)
    service = Service(
        cliente_id=1,
        descripcion="Recolección",
        estado="pendiente",
        fecha_solicitud=datetime.utcnow()
    )
    created = repo.create(service)
    assert created.id is not None
    assert created.estado == "pendiente"

    services = repo.list_all()
    assert len(services) == 1