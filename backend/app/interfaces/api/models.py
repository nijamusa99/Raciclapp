from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

# Auth
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    nombre: str
    telefono: Optional[str] = None
    rol: str  # validado en ruta
    nombre_edificio: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    tipo_vehiculo: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# User out
class UserOut(BaseModel):
    id: int
    email: str
    nombre: str
    rol: str
    activo: bool
    class Config:
        orm_mode = True

# Service
class ServiceCreate(BaseModel):
    descripcion: str

class ServiceOut(BaseModel):
    id: int
    cliente_id: int
    reciclador_id: Optional[int]
    descripcion: str
    estado: str
    fecha_solicitud: datetime
    fecha_asignacion: Optional[datetime]
    fecha_aceptacion: Optional[datetime]
    fecha_completado: Optional[datetime]
    class Config:
        orm_mode = True

# Rating
class RatingCreate(BaseModel):
    puntuacion: int
    @validator('puntuacion')
    def validar_rango(cls, v):
        if v < 1 or v > 5:
            raise ValueError('La puntuación debe estar entre 1 y 5')
        return v
    comentario: Optional[str] = None

class RatingOut(BaseModel):
    id: int
    servicio_id: int
    calificador_id: int
    calificado_id: int
    puntuacion: int
    comentario: Optional[str]
    fecha: datetime
    class Config:
        orm_mode = True

# Asignación
class AssignRequest(BaseModel):
    reciclador_id: int