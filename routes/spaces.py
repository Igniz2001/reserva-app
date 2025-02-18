#Este script es para el manejo de los espacios
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Espacio
from typing import List

from database import SessionLocal
from schemas import EspacioCreate, EspacioResponse

router = APIRouter()

# Se obtiene la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Función para crear un espacio nuevo
@router.post("/",response_model=EspacioResponse)
def crear_espacio(espacio: EspacioCreate, db: Session = Depends(get_db)):
    nuevo_espacio = Espacio(**espacio.dict())
    db.add(nuevo_espacio)
    db.commit()
    db.refresh(nuevo_espacio)
    return nuevo_espacio

#Para obtener todos los espacios
@router.get("/", response_model=List[EspacioResponse])
def obtener_espacios(db: Session = Depends(get_db)):
    return db.query(Espacio).all()