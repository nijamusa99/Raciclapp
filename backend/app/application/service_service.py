from datetime import datetime
from typing import List, Optional
from app.infrastructure.repositories.service_repo import ServiceRepository
from app.infrastructure.repositories.evidence_repo import EvidenceRepository
from app.infrastructure.repositories.rating_repo import RatingRepository
from app.infrastructure.models import Service, Evidence, Rating
from app.domain.enums import ServiceStatus

class ServiceService:
    def __init__(self,
                 service_repo: ServiceRepository,
                 evidence_repo: EvidenceRepository,
                 rating_repo: RatingRepository):
        self.service_repo = service_repo
        self.evidence_repo = evidence_repo
        self.rating_repo = rating_repo

    def create_service_request(self, cliente_id: int, descripcion: str) -> Service:
        service = Service(
            cliente_id=cliente_id,
            descripcion=descripcion,
            estado=ServiceStatus.PENDIENTE.value,
            fecha_solicitud=datetime.utcnow()
        )
        return self.service_repo.create(service)

    def assign_recycler(self, service_id: int, reciclador_id: int) -> Service:
        service = self.service_repo.get_by_id(service_id)
        if service.estado != ServiceStatus.PENDIENTE.value:
            raise ValueError("El servicio no está pendiente")
        service.reciclador_id = reciclador_id
        service.estado = ServiceStatus.ASIGNADO.value
        service.fecha_asignacion = datetime.utcnow()
        return self.service_repo.update(service)

    def accept_service(self, service_id: int, reciclador_id: int) -> Service:
        service = self.service_repo.get_by_id(service_id)
        if service.reciclador_id != reciclador_id or service.estado != ServiceStatus.ASIGNADO.value:
            raise ValueError("Acción no permitida")
        service.estado = ServiceStatus.ACEPTADO.value
        service.fecha_aceptacion = datetime.utcnow()
        return self.service_repo.update(service)

    def reject_service(self, service_id: int, reciclador_id: int) -> Service:
        service = self.service_repo.get_by_id(service_id)
        if service.reciclador_id != reciclador_id or service.estado != ServiceStatus.ASIGNADO.value:
            raise ValueError("Acción no permitida")
        service.estado = ServiceStatus.RECHAZADO.value
        return self.service_repo.update(service)

    def complete_service(self, service_id: int, reciclador_id: int, fotos_paths: List[str]) -> Service:
        service = self.service_repo.get_by_id(service_id)
        if service.reciclador_id != reciclador_id or service.estado != ServiceStatus.ACEPTADO.value:
            raise ValueError("No se puede completar en este estado")
        now = datetime.utcnow()
        evidence = Evidence(
            servicio_id=service_id,
            reciclador_id=reciclador_id,
            fotos=",".join(fotos_paths),  # guardar como string separado por comas
            timestamp_completado=now
        )
        self.evidence_repo.create(evidence)
        service.estado = ServiceStatus.COMPLETADO.value
        service.fecha_completado = now
        return self.service_repo.update(service)

    def rate_service(self, service_id: int, cliente_id: int, puntuacion: int, comentario: Optional[str] = None) -> Rating:
        service = self.service_repo.get_by_id(service_id)
        if service.cliente_id != cliente_id:
            raise ValueError("Solo el cliente puede calificar")
        if service.estado != ServiceStatus.COMPLETADO.value:
            raise ValueError("El servicio no está completado")
        if not service.reciclador_id:
            raise ValueError("No hay reciclador asignado")
        existing = self.rating_repo.get_by_service(service_id)
        if existing:
            raise ValueError("Ya se ha calificado este servicio")
        rating = Rating(
            servicio_id=service_id,
            calificador_id=cliente_id,
            calificado_id=service.reciclador_id,
            puntuacion=puntuacion,
            comentario=comentario,
            fecha=datetime.utcnow()
        )
        return self.rating_repo.create(rating)