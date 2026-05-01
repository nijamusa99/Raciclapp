from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.database import get_db
from app.infrastructure.repositories.user_repo import UserRepository
from app.infrastructure.repositories.service_repo import ServiceRepository
from app.infrastructure.repositories.rating_repo import RatingRepository
from app.application.service_service import ServiceService
from app.infrastructure.repositories.evidence_repo import EvidenceRepository
from app.interfaces.api.dependencies import require_role, get_current_user
from app.interfaces.api.models import UserOut, ServiceOut, RatingOut, AssignRequest
from app.infrastructure.models import User

router = APIRouter(dependencies=[Depends(require_role("superadmin"))])

@router.get("/usuarios", response_model=List[UserOut])
def listar_usuarios(rol: str = None, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    if rol:
        return repo.list_by_role(rol)
    return repo.list_all()

@router.get("/servicios", response_model=List[ServiceOut])
def listar_servicios(db: Session = Depends(get_db)):
    return ServiceRepository(db).list_all()

@router.get("/servicios/pendientes", response_model=List[ServiceOut])
def listar_pendientes(db: Session = Depends(get_db)):
    todos = ServiceRepository(db).list_all()
    return [s for s in todos if s.estado == "pendiente"]

@router.patch("/servicios/{id}/asignar", response_model=ServiceOut)
def asignar_servicio(id: int, data: AssignRequest, db: Session = Depends(get_db)):
    service_service = ServiceService(
        ServiceRepository(db),
        EvidenceRepository(db),
        RatingRepository(db)
    )
    try:
        return service_service.assign_recycler(id, data.reciclador_id)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@router.get("/calificaciones", response_model=List[RatingOut])
def ver_calificaciones(db: Session = Depends(get_db)):
    return RatingRepository(db).list_all()