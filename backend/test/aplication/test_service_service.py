from app.application.service_service import ServiceService
from app.infrastructure.repositories.service_repo import ServiceRepository
from app.infrastructure.repositories.evidence_repo import EvidenceRepository
from app.infrastructure.repositories.rating_repo import RatingRepository
from app.domain.enums import ServiceStatus

def test_service_lifecycle(db_session):
    sr = ServiceRepository(db_session)
    er = EvidenceRepository(db_session)
    rr = RatingRepository(db_session)
    service = ServiceService(sr, er, rr)

    # Crear servicio
    new_s = service.create_service_request(cliente_id=1, descripcion="Test")
    assert new_s.estado == ServiceStatus.PENDIENTE.value

    # Asignar reciclador
    assigned = service.assign_recycler(new_s.id, reciclador_id=2)
    assert assigned.estado == ServiceStatus.ASIGNADO.value

    # Aceptar
    accepted = service.accept_service(new_s.id, reciclador_id=2)
    assert accepted.estado == ServiceStatus.ACEPTADO.value

    # Completar
    completed = service.complete_service(new_s.id, reciclador_id=2, fotos_paths=["foto.jpg"])
    assert completed.estado == ServiceStatus.COMPLETADO.value

    # Calificar
    rating = service.rate_service(new_s.id, cliente_id=1, puntuacion=5, comentario="Bueno")
    assert rating.puntuacion == 5