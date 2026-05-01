from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, JSON, Text
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    telefono = Column(String, nullable=True)
    rol = Column(String, CheckConstraint("rol IN ('cliente','reciclador','superadmin')"), nullable=False)
    nombre_edificio = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    ciudad = Column(String, nullable=True)
    tipo_vehiculo = Column(String, nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    servicios_cliente = relationship("Service", back_populates="cliente", foreign_keys="Service.cliente_id")
    servicios_reciclador = relationship("Service", back_populates="reciclador", foreign_keys="Service.reciclador_id")

class Service(Base):
    __tablename__ = "servicios"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    reciclador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    descripcion = Column(String, nullable=False)
    estado = Column(String, CheckConstraint("estado IN ('pendiente','asignado','aceptado','rechazado','completado')"), nullable=False)
    fecha_solicitud = Column(DateTime, default=datetime.utcnow)
    fecha_asignacion = Column(DateTime, nullable=True)
    fecha_aceptacion = Column(DateTime, nullable=True)
    fecha_completado = Column(DateTime, nullable=True)

    cliente = relationship("User", back_populates="servicios_cliente", foreign_keys=[cliente_id])
    reciclador = relationship("User", back_populates="servicios_reciclador", foreign_keys=[reciclador_id])
    evidencia = relationship("Evidence", back_populates="servicio", uselist=False)
    calificacion = relationship("Rating", back_populates="servicio", uselist=False)

class Evidence(Base):
    __tablename__ = "evidencias_servicio"
    id = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey("servicios.id"), unique=True, nullable=False)
    reciclador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fotos = Column(Text, nullable=False)  # Comma-separated paths
    timestamp_completado = Column(DateTime, nullable=False)

    servicio = relationship("Service", back_populates="evidencia")

class Rating(Base):
    __tablename__ = "calificaciones"
    id = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey("servicios.id"), unique=True, nullable=False)
    calificador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    calificado_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    puntuacion = Column(Integer, CheckConstraint("puntuacion BETWEEN 1 AND 5"), nullable=False)
    comentario = Column(String, nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)

    servicio = relationship("Service", back_populates="calificacion")