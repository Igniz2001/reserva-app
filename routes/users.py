#Este script es para el manejo de los usuarios

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Usuario
from typing import List
from database import SessionLocal
from schemas import UsuarioCreate, UsuarioResponse
from models import Usuario

router = APIRouter()

# Se obtiene la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Función para crear un usuario nuevo
@router.post("/",response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.cedula == usuario.cedula).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="La cédula ya está registrada")
    nuevo_usuario = Usuario(**usuario.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

#Para obtener todos los usuarios
@router.get("/", response_model=List[UsuarioResponse])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()