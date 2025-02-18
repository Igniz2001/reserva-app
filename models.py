#Aquí se definen las entidades de la base de datos

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from database import Base


#Definición del modelo de Usuario

class Usuario(Base):
    __tablename__ = "usuarios"

    id= Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String, index=True)
    cedula = Column(String, unique=True, index=True)
    apartamento = Column(String)
    torre = Column(String)

    reservas = relationship("Reserva", back_populates="usuario")

#Definición del modelo de Espacio (sea Cancha, Salón social, etc.)
class Espacio(Base):
    __tablename__= "espacios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, nullable=True)
    estado = Column(String, default="Disponible") #Puede ser disponible o en mantenimiento dependiendo del lugar

    reservas = relationship("Reserva", back_populates="espacio")

#Definición del modelo de Reserva
class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    espacio_id = Column(Integer, ForeignKey("espacios.id"))
    fecha = Column(Date)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    estado = Column(String, default="Activa") #Puede ser Activa o Cancelada

    usuario = relationship("Usuario", back_populates="reservas")
    espacio = relationship("Espacio", back_populates="reservas")