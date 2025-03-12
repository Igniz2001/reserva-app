#Este script es para el manejo de las reservaciones
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Reserva, Usuario, Espacio
from database import SessionLocal
from schemas import ReservaCreate, ReservaResponse
from datetime import timedelta

router = APIRouter()

# Se obtiene la sesión de la base de datos
def get_db():
    """Obtiene la sesión de la base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para crear una reservación nueva
@router.post("/", response_model=ReservaResponse)
def crear_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    """Crea una nueva reservación en la base de datos"""
    db_usuario = db.query(Usuario).filter(Usuario.id == reserva.usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_espacio = db.query(Espacio).filter(Espacio.id == reserva.espacio_id).first()
    if db_espacio is None:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    nueva_reserva = Reserva(
        usuario_id=reserva.usuario_id,
        espacio_id=reserva.espacio_id,
        fecha=reserva.fecha,
        hora_inicio=reserva.hora_inicio,
        hora_fin=reserva.hora_fin,
        estado=reserva.estado
    )
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    return nueva_reserva

# Función para obtener una reservación por ID
@router.get("/{reserva_id}", response_model=ReservaResponse)
def obtener_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Obtiene una reservación por medio de su ID"""
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

# Función para modificar una reservación
@router.put("/{reserva_id}", response_model=ReservaResponse)
def modificar_reserva(reserva_id: int, reserva: ReservaCreate, db: Session = Depends(get_db)):
    """Modifica una reservación de la base de datos, identificandola primero por su ID"""
    db_reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    db_reserva.fecha = reserva.fecha
    db_reserva.hora_inicio = reserva.hora_inicio
    db_reserva.hora_fin = reserva.hora_fin
    db_reserva.espacio_id = reserva.espacio_id
    db_reserva.estado = reserva.estado
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

# Función para eliminar una reservación
@router.delete("/{reserva_id}")
def eliminar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Elimina una reservación de la base de datos, identificandola primero por su ID"""
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    db.delete(reserva)
    db.commit()
    return {"message": "Reserva eliminada"}

# Para obtener todas las reservaciones
@router.get("/", response_model=List[ReservaResponse])
def obtener_reservas(db: Session = Depends(get_db)):
    """Obtiene todas las reservaciones de la base de datos"""
    return db.query(Reserva).all()