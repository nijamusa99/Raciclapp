from enum import Enum

class UserRole(str, Enum):
    CLIENTE = "cliente"
    RECICLADOR = "reciclador"
    SUPERADMIN = "superadmin"

class ServiceStatus(str, Enum):
    PENDIENTE = "pendiente"
    ASIGNADO = "asignado"
    ACEPTADO = "aceptado"
    RECHAZADO = "rechazado"
    COMPLETADO = "completado"