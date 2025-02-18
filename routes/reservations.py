#Este script es para el manejo de las reservaciones
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Reserva, Usuario, Espacio
from database import SessionLocal
from schemas import ReservaCreate, ReservaResponse
from datetime import timedelta

router = APIRouter()

# Se obtiene la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Función para crear una reservación nueva
@router.post("/",response_model=ReservaResponse)
def crear_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    #Se verificará si el usuario tiene una reserva el mismo día
    db_usuario = db.query(Usuario).filter(Usuario.cedula == reserva.cedula).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db_espacio = db.query(Espacio).filter(Espacio.id == reserva.espacio_id).first()
    if not db_espacio or db_espacio.estado != "Disponible":
        raise HTTPException(status_code=400, detail="Espacio no disponible")
    
    reservas_usuarios = db.query(Reserva).filter(Reserva.usuario_id == db_usuario.id, Reserva.fecha == reserva.fecha).all()
    if len(reservas_usuarios) > 0:
        raise HTTPException(status_code=400, detail="Ya tiene una reserva en esta fecha")
    
    #Aquí se verifica si la reserva excede de 2 horas
    if (reserva.hora_fin - reserva.hora_inicio) > timedelta(hours=2):
        raise HTTPException(status_code=400, detail="La reserva no puede ser mayor a 2 horas")
    
    nueva_reserva = Reserva(**reserva.dict(), usuario_id=db_usuario.id)
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    return nueva_reserva