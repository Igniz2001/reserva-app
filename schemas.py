# Aquí se gestionan los datos que entran y salen de la base de datos

from pydantic import BaseModel
from datetime import datetime, time

# Esquema para crear un usuario
class UsuarioCreate(BaseModel):
    nombre_completo: str
    cedula: str
    apartamento: str
    torre: str

    class Config:
        orm_mode = True

# Esquema de respuesta para un usuario
class UsuarioResponse(BaseModel):
    id: int
    nombre_completo: str
    cedula: str
    apartamento: str
    torre: str

    class Config:
        orm_mode = True

# Esquema para crear un espacio
class EspacioCreate(BaseModel):
    nombre: str
    descripcion: str = None

    class Config:
        orm_mode = True

# Esquema de respuesta para un espacio
class EspacioResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    estado: str  # Ejemplo: Disponible, Reservado

    class Config:
        orm_mode = True

# Esquema para crear una reserva
class ReservaCreate(BaseModel):
    usuario_id: int
    espacio_id: int
    fecha: datetime
    hora_inicio: time
    hora_fin: time
    estado: str

    class Config:
        orm_mode = True

# Esquema de respuesta para una reserva
class ReservaResponse(BaseModel):
    id: int
    usuario_id: int
    espacio_id: int
    fecha: datetime
    hora_inicio: time
    hora_fin: time
    estado: str

    class Config:
        orm_mode = True