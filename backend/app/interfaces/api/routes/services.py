from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.repositories.service_repo import ServiceRepository
from app.infrastructure.repositories.evidence_repo import EvidenceRepository
from app.infrastructure.repositories.rating_repo import RatingRepository
from app.application.service_service import ServiceService
from app.interfaces.api.dependencies import get_current_user, require_role
from app.interfaces.api.models import ServiceCreate, ServiceOut, RatingCreate, RatingOut
from app.infrastructure.models import User

router = APIRouter(dependencies=[Depends(get_current_user)])

def get_service_service(db: Session = Depends(get_db)) -> ServiceService:
    return ServiceService(
        ServiceRepository(db),
        EvidenceRepository(db),
        RatingRepository(db)
    )

@router.post("/servicios", response_model=ServiceOut, dependencies=[Depends(require_role("cliente"))])
def crear_servicio(data: ServiceCreate,
                   current_user: User = Depends(get_current_user),
                   service: ServiceService = Depends(get_service_service)):
    ser = service.create_service_request(current_user.id, data.descripcion)
    return ser

@router.get("/servicios", response_model=list[ServiceOut])
def mis_servicios(current_user: User = Depends(get_current_user),
                  service: ServiceService = Depends(get_service_service),
                  db: Session = Depends(get_db)):
    repo = ServiceRepository(db)
    if current_user.rol == "cliente":
        return repo.list_by_client(current_user.id)
    elif current_user.rol == "reciclador":
        return repo.list_by_recycler(current_user.id)
    else:
        return repo.list_all()

@router.get("/servicios/{id}", response_model=ServiceOut)
def detalle_servicio(id: int,
                     current_user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    repo = ServiceRepository(db)
    ser = repo.get_by_id(id)
    if not ser:
        raise HTTPException(404, "Servicio no encontrado")
    if current_user.rol != "superadmin" and ser.cliente_id != current_user.id and ser.reciclador_id != current_user.id:
        raise HTTPException(403, "No autorizado")
    return ser

@router.post("/servicios/{id}/calificar", response_model=RatingOut, dependencies=[Depends(require_role("cliente"))])
def calificar_servicio(id: int,
                       data: RatingCreate,
                       current_user: User = Depends(get_current_user),
                       service: ServiceService = Depends(get_service_service)):
    try:
        rating = service.rate_service(id, current_user.id, data.puntuacion, data.comentario)
        return rating
    except ValueError as e:
        raise HTTPException(400, detail=str(e))