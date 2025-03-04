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
    """Obtiene la sesión de la base de datos"""	
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Función para crear un usuario nuevo
@router.post("/",response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario en la base de datos"""
    db_usuario = db.query(Usuario).filter(Usuario.cedula == usuario.cedula).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="La cédula ya está registrada")
    nuevo_usuario = Usuario(**usuario.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

#Función para obtener un usuario por ID
@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtiene un usuario por medio de su ID"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

#Función para modificar un usuario
@router.put("/{usuario_id}", response_model=UsuarioResponse)
def modificar_usuario(usuario_id: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Modifica un usuario de la base de datos, identificandolo primero por su ID"""
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_usuario.nombre_completo = usuario.nombre_completo
    db_usuario.cedula = usuario.cedula
    db_usuario.apartamento = usuario.apartamento
    db_usuario.torre = usuario.torre
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

#Función para eliminar un usuario
@router.delete("/{usuario_id}", response_model=dict)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Elimina un usuario de la base de datos, identificandolo primero por su ID"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado"}

#Para obtener todos los usuarios
@router.get("/", response_model=List[UsuarioResponse])
def obtener_usuarios(db: Session = Depends(get_db)):
    """Obtiene todos los usuarios de la base de datos"""
    return db.query(Usuario).all()