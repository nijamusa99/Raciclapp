from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os, uuid
from datetime import datetime
from app.infrastructure.database import get_db
from app.infrastructure.repositories.service_repo import ServiceRepository
from app.infrastructure.repositories.evidence_repo import EvidenceRepository
from app.infrastructure.repositories.rating_repo import RatingRepository
from app.application.service_service import ServiceService
from app.interfaces.api.dependencies import get_current_user, require_role
from app.interfaces.api.models import ServiceOut
from app.infrastructure.models import User
from app.config import settings

router = APIRouter(dependencies=[Depends(get_current_user), Depends(require_role("reciclador"))])

def get_service_service(db: Session = Depends(get_db)) -> ServiceService:
    return ServiceService(
        ServiceRepository(db),
        EvidenceRepository(db),
        RatingRepository(db)
    )

@router.get("/servicios", response_model=list[ServiceOut])
def servicios_asignados(current_user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    repo = ServiceRepository(db)
    todos = repo.list_by_recycler(current_user.id)
    # Mostrar solo los que están asignados o aceptados (pendientes de completar)
    return [s for s in todos if s.estado in ("asignado", "aceptado")]

@router.patch("/servicios/{id}/aceptar", response_model=ServiceOut)
def aceptar_servicio(id: int,
                     current_user: User = Depends(get_current_user),
                     service: ServiceService = Depends(get_service_service)):
    try:
        return service.accept_service(id, current_user.id)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@router.patch("/servicios/{id}/rechazar", response_model=ServiceOut)
def rechazar_servicio(id: int,
                      current_user: User = Depends(get_current_user),
                      service: ServiceService = Depends(get_service_service)):
    try:
        return service.reject_service(id, current_user.id)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@router.post("/servicios/{id}/completar")
async def completar_servicio(id: int,
                             fotos: List[UploadFile] = File(...),
                             current_user: User = Depends(get_current_user),
                             service: ServiceService = Depends(get_service_service),
                             db: Session = Depends(get_db)):
    # Verificar que el servicio esté aceptado y pertenezca al reciclador
    repo = ServiceRepository(db)
    ser = repo.get_by_id(id)
    if not ser or ser.reciclador_id != current_user.id or ser.estado != "aceptado":
        raise HTTPException(400, detail="No se puede completar en este estado")
    # Guardar archivos
    upload_dir = os.path.join(settings.UPLOAD_DIR, str(id))
    os.makedirs(upload_dir, exist_ok=True)
    paths = []
    for foto in fotos:
        if foto.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(400, detail="Solo se permiten imágenes JPG/PNG")
        ext = os.path.splitext(foto.filename)[1]
        new_name = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(upload_dir, new_name)
        with open(file_path, "wb") as f:
            content = await foto.read()
            f.write(content)
        paths.append(file_path)
    try:
        updated = service.complete_service(id, current_user.id, paths)
        return {"mensaje": "Servicio completado", "servicio": updated}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))