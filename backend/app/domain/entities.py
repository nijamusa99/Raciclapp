from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from .enums import UserRole, ServiceStatus

class Usuario(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    nombre: str
    telefono: Optional[str] = None
    rol: UserRole
    nombre_edificio: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    tipo_vehiculo: Optional[str] = None
    activo: bool = True
    created_at: Optional[datetime] = None

class Servicio(BaseModel):
    id: Optional[int] = None
    cliente_id: int
    reciclador_id: Optional[int] = None
    descripcion: str
    estado: ServiceStatus = ServiceStatus.PENDIENTE
    fecha_solicitud: Optional[datetime] = None
    fecha_asignacion: Optional[datetime] = None
    fecha_aceptacion: Optional[datetime] = None
    fecha_completado: Optional[datetime] = None

class Evidencia(BaseModel):
    id: Optional[int] = None
    servicio_id: int
    reciclador_id: int
    fotos: List[str]
    timestamp_completado: datetime

class Calificacion(BaseModel):
    id: Optional[int] = None
    servicio_id: int
    calificador_id: int
    calificado_id: int
    puntuacion: int
    comentario: Optional[str] = None
    fecha: Optional[datetime] = None