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
    """Obtiene la sesión de la base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Función para crear un espacio nuevo
@router.post("/",response_model=EspacioResponse)
def crear_espacio(espacio: EspacioCreate, db: Session = Depends(get_db)):
    """Crea un nuevo espacio en la base de datos"""
    nuevo_espacio = Espacio(**espacio.dict())
    db.add(nuevo_espacio)
    db.commit()
    db.refresh(nuevo_espacio)
    return nuevo_espacio

#Función para obtener un espacio por ID
@router.get("/{id}", response_model=EspacioResponse)
def obtener_espacio(id: int, db: Session = Depends(get_db)):
    """Obtiene un espacio de la base de datos por su ID"""	
    espacio = db.query(Espacio).filter(Espacio.id == id).first()
    if not espacio:
        raise HTTPException(status_code=404, detail="El espacio no existe")
    return espacio

#Función para eliminar un espacio por ID
@router.delete("/{id}")
def eliminar_espacio(id: int, db: Session = Depends(get_db)):
    """Elimina un espacio de la base de datos, identificandolo primero por su ID"""
    espacio = db.query(Espacio).filter(Espacio.id == id).first()
    if not espacio:
        raise HTTPException(status_code=404, detail="El espacio no existe")
    db.delete(espacio)
    db.commit()
    return {"message": "Espacio eliminado"}

#Función para modificar un espacio por ID
@router.put("/{id}", response_model=EspacioResponse)
def modificar_espacio(id: int, espacio: EspacioCreate, db: Session = Depends(get_db)):
    """Modifica un espacio de la base de datos, identificandolo primero por su ID"""
    espacio_db = db.query(Espacio).filter(Espacio.id == id).first()
    if not espacio_db:
        raise HTTPException(status_code=404, detail="El espacio no existe")
    espacio_db.nombre = espacio.nombre
    espacio_db.descripcion = espacio.descripcion
    db.commit()
    db.refresh(espacio_db)
    return espacio_db

#Para obtener todos los espacios
@router.get("/", response_model=List[EspacioResponse])
def obtener_espacios(db: Session = Depends(get_db)):
    """Obtiene todos los espacios de la base de datos"""	
    return db.query(Espacio).all()